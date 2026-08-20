import time
from typing import TypeVar

import litellm
from pydantic import BaseModel

from .config import AiConfig

T = TypeVar("T", bound=BaseModel)


class AiGateway:
    """Thin wrapper exposing the relevant AI API calls."""

    def __init__(self, config: AiConfig) -> None:
        self.config = config
        self.max_retries = 3

    def chat(
        self,
        prompt: str,
        system_prompt: str,
        response_type: type[T],
    ) -> T:
        for attempt in range(self.max_retries):
            try:
                return litellm.completion(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    response_type=response_type,
                    **self.config.kwargs,
                )

            except (litellm.Timeout, litellm.RateLimitError) as exc:
                if attempt >= self.max_retries - 1:
                    raise ValueError(
                        f"Model request failed after {attempt} attempts."
                    ) from exc
                time.sleep(3)
