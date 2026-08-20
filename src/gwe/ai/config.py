from typing import Any

import litellm
from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
)


class AiConfig(BaseModel):
    """Configuration for users chosen AI provider."""

    kwargs: dict[str, Any] = Field(default_factory=dict)
    model: str

    @field_validator("model")
    @classmethod
    def validate_model(cls, model: str, info: ValidationInfo) -> str:
        """Ensure the selected model supports structured outputs."""
        kwargs = info.data.get("kwargs", {})

        try:
            if not litellm.supports_response_schema(
                model=model,
                custom_llm_provider=kwargs.get("custom_llm_provider"),
            ):
                raise ValueError(
                    f"Model '{model}' does not support Pydantic response formats."
                )
        except Exception:  # noqa: BLE001 # i cant plan for the ambiguous errors this could cause...
            raise ValueError(
                f"Unable to determine support for pydantic response formats for model {model}."
            )

        return model
