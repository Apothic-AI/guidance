from __future__ import annotations

from typing import Iterator

from .._ast import GrammarNode, RegexNode
from ..trace import OutputAttr, TextOutput, TokenOutput
from ._openai_base import BaseOpenAIInterpreter


class OpenRouterGrammarMixin(BaseOpenAIInterpreter):
    def regex(self, node: RegexNode, **kwargs) -> Iterator[OutputAttr]:
        if not self._is_openrouter_client():
            return super().regex(node, **kwargs)

        if node.regex is None:
            # Unconstrained generation path.
            return self._run(**kwargs)
        return self.grammar(node, **kwargs)

    def grammar(self, node: GrammarNode, **kwargs) -> Iterator[OutputAttr]:
        if not self._is_openrouter_client():
            return super().grammar(node, **kwargs)

        openrouter_kwargs = self._apply_openrouter_request_overrides(dict(kwargs))
        if not self._openrouter_supports_grammar_response_format(openrouter_kwargs):
            raise ValueError(
                f"OpenRouter model '{self.model}' does not support grammar response formats "
                "for the current provider routing."
            )

        grammar_definition = node.ll_grammar()
        generated_text = ""
        try:
            for attr in self._run(
                response_format={
                    "type": "grammar",
                    "grammar": grammar_definition,
                },
                **kwargs,
            ):
                if isinstance(attr, (TextOutput, TokenOutput)):
                    generated_text += attr.value
                yield attr
        except Exception as exc:  # noqa: BLE001
            message = str(exc).lower()
            grammar_markers = (
                "grammar",
                "response_format",
                "structured output",
                "structured_output",
            )
            unsupported_markers = ("unsupported", "not support", "invalid", "provider returned error")
            if any(marker in message for marker in grammar_markers) and any(
                marker in message for marker in unsupported_markers
            ):
                raise ValueError(
                    f"OpenRouter provider for model '{self.model}' rejected grammar-constrained generation."
                ) from exc
            raise

        matches = node.match(
            generated_text,
            raise_exceptions=False,
            # We cannot enforce token limits here because OpenRouter tokenization is provider-specific.
            enforce_max_tokens=False,
        )
        if matches is None:
            raise ValueError(
                f"OpenRouter provider output for model '{self.model}' failed local grammar validation."
            )

        for name, value in matches.captures.items():
            log_probs = matches.log_probs[name]
            if isinstance(value, list):
                assert isinstance(log_probs, list)
                assert len(value) == len(log_probs)
                for v, l in zip(value, log_probs, strict=True):
                    yield self.state.apply_capture(name=name, value=v, log_prob=l, is_append=True)
            else:
                yield self.state.apply_capture(name=name, value=value, log_prob=log_probs, is_append=False)
