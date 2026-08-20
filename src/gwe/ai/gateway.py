import time
from importlib.resources import files

from typing import (
    Any,
    TypeVar
)

import litellm

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidationInfo,
)


T = TypeVar("T", bound=BaseModel)


class AiConfig(BaseModel):
    """Configuration for users chosen AI provider."""
    kwargs: dict[str, Any] = Field(default_factory=dict)
    model: str

    @field_validator("model")
    @classmethod
    def validate_model(cls, model: str, info: ValidationInfo) -> str:
        """Ensure the selected model supports strucutred outputs or the whole thing
        will inevitably fail anyways.
        """
        kwargs = info.data.get("kwargs", {})

        try:
            if not litellm.supports_response_schema(
                model=model,
                custom_llm_provider=kwargs.get("custom_llm_provider"),
            ):
                raise ValueError(
                    f"Model '{model}' does not support Pydantic response formats."
                )
        except Exception:
            raise ValueError(
                f"Unable to determine support for pydantic response formats for model {model}."
            )

        return model


class AiGateway():
    """Thin wrapper exposing the relevant AI API calls."""
    def __init__(
        self,
        config: AiConfig
    ) -> None:
        self.config = config
        self.max_retries = 3

        self._system_prompt = (
            files("gwe.ai")
            .joinpath("prompts", "triplet_extraction_v2.txt")
            .read_text(encoding="utf-8")
        )

    def chat(
        self, 
        prompt: str,
        response_type: type[T]
    ) -> T:
        for attempt in range(self.max_retries):
            try: 
                # i think litellm actually has a retry loop built in, but since this abstraction exists to future
                # proof us, we'll include a manual one anyway
                return litellm.completion(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": self._system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    response_type=response_type,
                    **self.config.kwargs,
                )
            
            except (litellm.Timeout, litellm.RateLimitError) as exc:
                if attempt >= self.max_retries-1:
                    raise ValueError(
                        f"Model request failed after "
                        f"{attempt} attempts."
                    ) from exc
                time.sleep(3)
