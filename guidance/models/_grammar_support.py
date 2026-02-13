from __future__ import annotations

import json
import re
import warnings
from typing import Any, cast

from .._ast import (
    GrammarNode,
    JoinNode,
    LiteralNode,
    RegexNode,
    RepeatNode,
    RuleNode,
    RuleRefNode,
    SelectNode,
)
from ..trace import OutputAttr
from ._base import State


class ConstraintProviderRejectedError(ValueError):
    """Raised when a provider rejects a constrained-generation request."""


class ConstraintValidationFailedError(ValueError):
    """Raised when provider output fails local Guidance validation."""


class ConstraintUnsupportedFeatureError(ValueError):
    """Raised when a grammar cannot be translated to the provider syntax."""


def apply_local_constraint_validation(
    *,
    node: GrammarNode,
    generated_text: str,
    state: State,
    model: str,
    provider: str,
) -> list[OutputAttr]:
    matches = node.match(
        generated_text,
        raise_exceptions=False,
        # Remote providers may tokenize differently than Guidance local parser.
        enforce_max_tokens=False,
    )
    if matches is None:
        raise ConstraintValidationFailedError(
            f"{provider} provider output for model '{model}' failed local grammar validation."
        )

    outputs: list[OutputAttr] = []
    for name, value in matches.captures.items():
        log_probs = matches.log_probs[name]
        if isinstance(value, list):
            if not isinstance(log_probs, list) or len(value) != len(log_probs):
                raise ConstraintValidationFailedError(
                    f"{provider} provider output for model '{model}' returned invalid capture log-prob metadata."
                )
            for v, l in zip(value, log_probs, strict=True):
                outputs.append(state.apply_capture(name=name, value=v, log_prob=l, is_append=True))
        else:
            outputs.append(state.apply_capture(name=name, value=value, log_prob=cast(float | None, log_probs)))
    return outputs


def looks_like_provider_rejection_error(message: str) -> bool:
    lowered = str(message).lower()
    grammar_markers = ("grammar", "response_format", "structured output", "structured_output", "custom tool")
    unsupported_markers = ("unsupported", "not support", "invalid", "provider returned error", "unknown")
    return any(marker in lowered for marker in grammar_markers) and any(
        marker in lowered for marker in unsupported_markers
    )


def _normalize_rule_name(name: str, *, default: str = "rule") -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]", "_", str(name).strip())
    if not normalized:
        normalized = default
    if normalized[0].isdigit():
        normalized = f"{default}_{normalized}"
    return normalized.lower()


class OpenAIResponsesGrammarBuilder:
    """Build OpenAI Responses custom-tool grammar format from Guidance grammar nodes."""

    def build(self, node: GrammarNode) -> dict[str, str]:
        if isinstance(node, RegexNode):
            if node.regex is None:
                raise ConstraintUnsupportedFeatureError("Unconstrained regex nodes cannot be mapped to OpenAI grammar.")
            return {
                "type": "grammar",
                "syntax": "regex",
                "definition": node.regex,
            }

        if isinstance(node, SelectNode) and all(isinstance(alt, LiteralNode) for alt in node.alternatives):
            literals = [cast(LiteralNode, alt).value for alt in node.alternatives]
            escaped = "|".join(re.escape(value) for value in literals)
            return {
                "type": "grammar",
                "syntax": "regex",
                "definition": f"(?:{escaped})",
            }

        return {
            "type": "grammar",
            "syntax": "lark",
            "definition": _OpenAILarkSubsetSerializer().serialize(node),
        }


class _OpenAILarkSubsetSerializer:
    def __init__(self) -> None:
        self._rule_names: dict[RuleNode, str] = {}
        self._rule_definitions: dict[str, str] = {}

    def serialize(self, node: GrammarNode) -> str:
        if isinstance(node, RuleNode) and _normalize_rule_name(node.name, default="start") == "start":
            start_name = self._visit_rule(node)
        else:
            start_name = "start"
            self._rule_definitions[start_name] = self._visit_expr(node, nested=False)

        lines = [f"{name}: {body}" for name, body in self._rule_definitions.items()]
        if start_name != "start" and "start" not in self._rule_definitions:
            lines.insert(0, f"start: {start_name}")
        return "\n".join(lines)

    def _unsupported_attrs(self, node: RuleNode) -> list[str]:
        unsupported: list[str] = []
        if node.temperature is not None:
            unsupported.append("temperature")
        if node.max_tokens is not None:
            unsupported.append("max_tokens")
        if node.stop is not None:
            unsupported.append("stop")
        if node.suffix is not None:
            unsupported.append("suffix")
        if node.stop_capture is not None:
            unsupported.append("stop_capture")
        if node.lazy:
            unsupported.append("lazy")
        return unsupported

    def _visit_rule(self, node: RuleNode) -> str:
        unsupported_attrs = self._unsupported_attrs(node)
        if unsupported_attrs:
            joined = ", ".join(unsupported_attrs)
            raise ConstraintUnsupportedFeatureError(f"OpenAI Lark adapter does not support RuleNode attrs: {joined}.")

        existing = self._rule_names.get(node)
        if existing is not None:
            return existing

        base = _normalize_rule_name(node.name, default="rule")
        if base == "start":
            name = "start"
        else:
            name = base
            i = 1
            while name in self._rule_definitions:
                i += 1
                name = f"{base}_{i}"
        self._rule_names[node] = name
        self._rule_definitions[name] = self._visit_expr(node.value, nested=False)
        return name

    def _visit_expr(self, node: GrammarNode, *, nested: bool) -> str:
        if isinstance(node, RuleNode):
            return self._visit_rule(node)
        if isinstance(node, RuleRefNode):
            if node.target is None:
                raise ConstraintUnsupportedFeatureError("RuleRefNode has no target.")
            return self._visit_rule(node.target)
        if isinstance(node, LiteralNode):
            return json.dumps(node.value)
        if isinstance(node, RegexNode):
            if node.regex is None:
                raise ConstraintUnsupportedFeatureError("Unconstrained regex nodes cannot be mapped to OpenAI Lark.")
            escaped = re.sub(r"(?<!\\)/", r"\/", node.regex).replace("\n", "\\n")
            return f"/{escaped}/"
        if isinstance(node, JoinNode):
            parts = [self._visit_expr(part, nested=True) for part in node.nodes if not part.is_null]
            return " ".join(parts) if parts else '""'
        if isinstance(node, SelectNode):
            body = " | ".join(self._visit_expr(alt, nested=True) for alt in node.alternatives)
            return f"({body})" if nested else body
        if isinstance(node, RepeatNode):
            base = self._visit_expr(node.node, nested=True)
            base_grouped = f"({base})" if " " in base or "|" in base else base
            if (node.min, node.max) == (0, None):
                return f"{base_grouped}*"
            if (node.min, node.max) == (1, None):
                return f"{base_grouped}+"
            if (node.min, node.max) == (0, 1):
                return f"{base_grouped}?"
            if node.max is not None and node.max < node.min:
                raise ConstraintUnsupportedFeatureError("RepeatNode max must be >= min.")
            if node.max is not None and node.max - node.min > 32:
                raise ConstraintUnsupportedFeatureError(
                    "OpenAI Lark adapter refuses very wide bounded repeats (max-min > 32)."
                )
            if node.max is None:
                required = " ".join(base_grouped for _ in range(node.min))
                if node.min == 0:
                    return f"{base_grouped}*"
                if node.min == 1:
                    return f"{base_grouped}+"
                tail = f"{base_grouped}*"
                return f"{required} {tail}".strip()
            if node.min == node.max:
                return " ".join(base_grouped for _ in range(node.min)) or '""'
            variants = []
            for count in range(node.min, node.max + 1):
                variants.append(" ".join(base_grouped for _ in range(count)) or '""')
            joined = " | ".join(variants)
            return f"({joined})"

        raise ConstraintUnsupportedFeatureError(
            f"OpenAI Lark adapter does not support node type: {type(node).__name__}."
        )


class FireworksGBNFBuilder:
    """Build Fireworks grammar payloads using a conservative GBNF subset."""

    def build(self, node: GrammarNode) -> str:
        serializer = _GBNFSubsetSerializer()
        return serializer.serialize(node)


class _GBNFSubsetSerializer:
    def __init__(self) -> None:
        self._rule_names: dict[RuleNode, str] = {}
        self._rule_definitions: dict[str, str] = {}

    def serialize(self, node: GrammarNode) -> str:
        if isinstance(node, RuleNode) and _normalize_rule_name(node.name, default="root") == "root":
            root_name = self._visit_rule(node)
        else:
            root_name = "root"
            self._rule_definitions[root_name] = self._visit_expr(node, nested=False)

        lines = [f"{name} ::= {body}" for name, body in self._rule_definitions.items()]
        if root_name != "root" and "root" not in self._rule_definitions:
            lines.insert(0, f"root ::= {root_name}")
        return "\n".join(lines)

    def _unsupported_attrs(self, node: RuleNode) -> list[str]:
        unsupported: list[str] = []
        if node.temperature is not None:
            unsupported.append("temperature")
        if node.max_tokens is not None:
            unsupported.append("max_tokens")
        if node.stop is not None:
            unsupported.append("stop")
        if node.suffix is not None:
            unsupported.append("suffix")
        if node.stop_capture is not None:
            unsupported.append("stop_capture")
        if node.lazy:
            unsupported.append("lazy")
        return unsupported

    def _visit_rule(self, node: RuleNode) -> str:
        unsupported_attrs = self._unsupported_attrs(node)
        if unsupported_attrs:
            joined = ", ".join(unsupported_attrs)
            raise ConstraintUnsupportedFeatureError(f"Fireworks GBNF adapter does not support RuleNode attrs: {joined}.")

        existing = self._rule_names.get(node)
        if existing is not None:
            return existing

        base = _normalize_rule_name(node.name, default="rule")
        if base == "root":
            name = "root"
        else:
            name = base
            i = 1
            while name in self._rule_definitions:
                i += 1
                name = f"{base}_{i}"
        self._rule_names[node] = name
        self._rule_definitions[name] = self._visit_expr(node.value, nested=False)
        return name

    def _visit_expr(self, node: GrammarNode, *, nested: bool) -> str:
        if isinstance(node, RuleNode):
            return self._visit_rule(node)
        if isinstance(node, RuleRefNode):
            if node.target is None:
                raise ConstraintUnsupportedFeatureError("RuleRefNode has no target.")
            return self._visit_rule(node.target)
        if isinstance(node, LiteralNode):
            return json.dumps(node.value)
        if isinstance(node, RegexNode):
            if node.regex is None:
                raise ConstraintUnsupportedFeatureError("Unconstrained regex nodes cannot be mapped to Fireworks GBNF.")
            return _regex_to_gbnf_expression(node.regex)
        if isinstance(node, JoinNode):
            parts = [self._visit_expr(part, nested=True) for part in node.nodes if not part.is_null]
            return " ".join(parts) if parts else '""'
        if isinstance(node, SelectNode):
            body = " | ".join(self._visit_expr(alt, nested=True) for alt in node.alternatives)
            return f"({body})" if nested else body
        if isinstance(node, RepeatNode):
            inner = self._visit_expr(node.node, nested=True)
            inner_grouped = f"({inner})" if " " in inner or "|" in inner else inner
            return _repeat_to_ebnf(inner_grouped, node.min, node.max)

        raise ConstraintUnsupportedFeatureError(
            f"Fireworks GBNF adapter does not support node type: {type(node).__name__}."
        )


def _repeat_to_ebnf(inner: str, min_count: int, max_count: int | None) -> str:
    if min_count < 0:
        raise ConstraintUnsupportedFeatureError("Repeat minimum must be >= 0.")
    if max_count is not None and max_count < min_count:
        raise ConstraintUnsupportedFeatureError("Repeat maximum must be >= minimum.")
    if (min_count, max_count) == (0, None):
        return f"{inner}*"
    if (min_count, max_count) == (1, None):
        return f"{inner}+"
    if (min_count, max_count) == (0, 1):
        return f"{inner}?"

    if max_count is None:
        required = " ".join(inner for _ in range(min_count))
        if min_count == 0:
            return f"{inner}*"
        if min_count == 1:
            return f"{inner}+"
        return f"{required} {inner}*".strip()

    if max_count - min_count > 16:
        raise ConstraintUnsupportedFeatureError("Bounded repeat ranges wider than 16 are not supported in GBNF adapter.")

    variants = []
    for count in range(min_count, max_count + 1):
        variants.append(" ".join(inner for _ in range(count)) or '""')
    if len(variants) == 1:
        return variants[0]
    return "(" + " | ".join(variants) + ")"


def _escape_char_class_char(ch: str) -> str:
    if ch in ("\\", "]", "-", "^"):
        return "\\" + ch
    if ch == "\n":
        return "\\n"
    if ch == "\r":
        return "\\r"
    if ch == "\t":
        return "\\t"
    return ch


def _regex_char_class(items: list[tuple[Any, Any]]) -> str:
    sre_parse = _import_sre_parse()

    parts: list[str] = []
    negated = False
    for op, arg in items:
        if op == sre_parse.NEGATE:
            negated = True
            continue
        if op == sre_parse.LITERAL:
            parts.append(_escape_char_class_char(chr(cast(int, arg))))
            continue
        if op == sre_parse.RANGE:
            lo, hi = cast(tuple[int, int], arg)
            parts.append(f"{_escape_char_class_char(chr(lo))}-{_escape_char_class_char(chr(hi))}")
            continue
        if op == sre_parse.CATEGORY:
            if arg == sre_parse.CATEGORY_DIGIT:
                parts.append("0-9")
                continue
            if arg == sre_parse.CATEGORY_WORD:
                parts.append("A-Za-z0-9_")
                continue
            if arg == sre_parse.CATEGORY_SPACE:
                parts.append(" \\t\\n\\r")
                continue
        raise ConstraintUnsupportedFeatureError(f"Unsupported regex char-class construct for GBNF: {op!r}.")

    if negated:
        raise ConstraintUnsupportedFeatureError("Negated regex character classes are not yet supported in GBNF adapter.")
    return "[" + "".join(parts) + "]"


def _regex_tokens_to_gbnf(tokens: list[tuple[Any, Any]]) -> str:
    sre_parse = _import_sre_parse()

    parts: list[str] = []
    for op, arg in tokens:
        if op == sre_parse.LITERAL:
            parts.append(json.dumps(chr(cast(int, arg))))
            continue
        if op == sre_parse.IN:
            parts.append(_regex_char_class(cast(list[tuple[Any, Any]], arg)))
            continue
        if op == sre_parse.ANY:
            parts.append("[\\x00-\\x7F]")
            continue
        if op == sre_parse.SUBPATTERN:
            sub = cast(tuple[Any, Any, Any, Any], arg)[3]
            sub_expr = _regex_tokens_to_gbnf(list(sub))
            parts.append(f"({sub_expr})")
            continue
        if op in (sre_parse.MAX_REPEAT, sre_parse.MIN_REPEAT):
            min_count, max_count, inner = cast(tuple[int, int, Any], arg)
            if max_count == sre_parse.MAXREPEAT:
                max_count = None
            inner_expr = _regex_tokens_to_gbnf(list(inner))
            inner_grouped = f"({inner_expr})" if " " in inner_expr or "|" in inner_expr else inner_expr
            parts.append(_repeat_to_ebnf(inner_grouped, min_count, max_count))
            continue
        if op == sre_parse.BRANCH:
            _, branches = cast(tuple[Any, list[Any]], arg)
            branch_exprs = [_regex_tokens_to_gbnf(list(branch)) for branch in branches]
            parts.append("(" + " | ".join(branch_exprs) + ")")
            continue
        if op == sre_parse.AT:
            # Start/end anchors are implicit in a dedicated constrained-generation call.
            continue
        raise ConstraintUnsupportedFeatureError(f"Unsupported regex construct for GBNF adapter: {op!r}.")

    return " ".join(parts) if parts else '""'


def _regex_to_gbnf_expression(pattern: str) -> str:
    sre_parse = _import_sre_parse()

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            parsed = sre_parse.parse(pattern)
    except re.error as exc:
        raise ConstraintUnsupportedFeatureError(f"Invalid regex for GBNF adapter: {exc}") from exc

    expr = _regex_tokens_to_gbnf(list(parsed.data))
    if expr == "":
        return '""'
    return expr


def _import_sre_parse():  # noqa: ANN201
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            import sre_parse
    except Exception as exc:  # noqa: BLE001
        raise ConstraintUnsupportedFeatureError("Python regex parser is unavailable for GBNF regex conversion.") from exc
    return sre_parse
