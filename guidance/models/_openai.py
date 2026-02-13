from guidance._schema import SamplingParams

from ._base import Model
from ._openai_base import (
    BaseOpenAIInterpreter,
    OpenAIAudioMixin,
    OpenAIClientWrapper,
    OpenAIImageMixin,
    OpenAIJSONMixin,
    OpenAIRegexMixin,
    OpenAIRuleMixin,
)
from ._openrouter_capabilities import (
    _extract_openrouter_model_modalities,
    _normalized_openrouter_api_base,
    resolve_openrouter_model_metadata,
)


class OpenAIInterpreter(OpenAIRuleMixin, OpenAIJSONMixin, OpenAIRegexMixin, BaseOpenAIInterpreter):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        reasoning_effort: str | None = None,
        openrouter_require_parameters: bool | None = None,
        openrouter_allow_fallbacks: bool | None = None,
        openrouter_provider: str | None = None,
        **kwargs,
    ):
        try:
            import openai
        except ImportError as ie:
            raise Exception(
                "Please install the openai package version >= 1 using `pip install openai -U` in order to use guidance.models.OpenAI!"
            ) from ie

        client = openai.OpenAI(api_key=api_key, **kwargs)
        super().__init__(model=model, client=OpenAIClientWrapper(client), reasoning_effort=reasoning_effort)
        self.openrouter_require_parameters = openrouter_require_parameters
        self.openrouter_allow_fallbacks = openrouter_allow_fallbacks
        self.openrouter_provider = openrouter_provider


class OpenAI(Model):
    def __init__(
        self,
        model: str,
        sampling_params: SamplingParams | None = None,
        echo: bool = True,
        *,
        api_key: str | None = None,
        reasoning_effort: str | None = None,
        openrouter_require_parameters: bool | None = None,
        openrouter_allow_fallbacks: bool | None = None,
        openrouter_provider: str | None = None,
        **kwargs,
    ):
        """Build a new OpenAI model object that represents a model in a given state.

        Parameters
        ----------
        model : str
            The name of the OpenAI model to use (e.g. gpt-4o-mini).
        echo : bool
            If true the final result of creating this model state will be displayed (as HTML in a notebook).
        api_key : None or str
            The OpenAI API key to use for remote requests, passed directly to the `openai.OpenAI` constructor.

        **kwargs :
            All extra keyword arguments are passed directly to the `openai.OpenAI` constructor. Commonly used argument
            names include `base_url` and `organization`
        """

        base_url = str(kwargs.get("base_url", "")).strip().lower()
        using_openrouter = "openrouter.ai" in base_url

        has_audio = False
        has_image = False
        if using_openrouter:
            model_meta = resolve_openrouter_model_metadata(
                model=model,
                api_base=_normalized_openrouter_api_base(base_url),
                api_key=api_key or "",
            )
            input_modalities, output_modalities = _extract_openrouter_model_modalities(model_meta)
            has_audio = "audio" in input_modalities or "audio" in output_modalities
            has_image = "image" in input_modalities

        if not using_openrouter:
            has_audio = "audio-preview" in model
            has_image = model.startswith("gpt-4o") or model.startswith("o1")
        else:
            if not has_audio and not has_image and "audio-preview" in model:
                has_audio = True
            if not has_audio and not has_image and (model.startswith("gpt-4o") or model.startswith("o1")):
                has_image = True

        if has_audio and has_image:
            interpreter_cls = type("OpenAIAudioImageInterpreter", (OpenAIAudioMixin, OpenAIImageMixin, OpenAIInterpreter), {})
        elif has_audio:
            interpreter_cls = type("OpenAIAudioInterpreter", (OpenAIAudioMixin, OpenAIInterpreter), {})
        elif has_image:
            interpreter_cls = type("OpenAIImageInterpreter", (OpenAIImageMixin, OpenAIInterpreter), {})
        else:
            interpreter_cls = OpenAIInterpreter

        super().__init__(
            interpreter=interpreter_cls(
                model,
                api_key=api_key,
                reasoning_effort=reasoning_effort,
                openrouter_require_parameters=openrouter_require_parameters,
                openrouter_allow_fallbacks=openrouter_allow_fallbacks,
                openrouter_provider=openrouter_provider,
                **kwargs,
            ),
            sampling_params=SamplingParams() if sampling_params is None else sampling_params,
            echo=echo,
        )
