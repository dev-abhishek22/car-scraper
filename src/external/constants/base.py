from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

HttpMethod = Literal[
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
]


@dataclass(frozen=True, slots=True)
class ApiEndpoint:
    name: str
    method: HttpMethod
    path: str
    default_params: dict[str, Any] = field(default_factory=dict)
    default_headers: dict[str, str] = field(default_factory=dict)
    expected_response: Literal[
        "json",
        "text",
        "bytes",
    ] = "json"
