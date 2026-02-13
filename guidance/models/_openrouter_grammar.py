from __future__ import annotations

from typing import Iterator

from .._ast import GrammarNode, RegexNode
from ..trace import OutputAttr, TextOutput, TokenOutput
from ._grammar_support import (
    ConstraintProviderRejectedError,
    ConstraintUnsupportedFeatureError,
    FireworksGBNFBuilder,
    apply_local_constraint_validation,
    looks_like_provider_rejection_error,
)
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

        grammar_format = self._openrouter_grammar_format_for_request(openrouter_kwargs)
        try:
            if grammar_format == "gbnf":
                grammar_definition = FireworksGBNFBuilder().build(node)
            else:
                grammar_definition = node.ll_grammar()
        except ConstraintUnsupportedFeatureError as exc:
            raise ValueError(
                f"OpenRouter provider grammar adapter '{grammar_format}' cannot represent this Guidance grammar."
            ) from exc
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
            if looks_like_provider_rejection_error(str(exc)):
                raise ConstraintProviderRejectedError(
                    f"OpenRouter provider for model '{self.model}' rejected grammar-constrained generation."
                ) from exc
            raise

        yield from apply_local_constraint_validation(
            node=node,
            generated_text=generated_text,
            state=self.state,
            model=self.model,
            provider="OpenRouter",
        )
