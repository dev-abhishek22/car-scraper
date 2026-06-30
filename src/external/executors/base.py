from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseApiExecutor(ABC):
    @abstractmethod
    def execute(
        self,
        **kwargs: Any,
    ) -> dict[str, Any] | list[Any]:
        """Execute an external API request."""
        raise NotImplementedError
