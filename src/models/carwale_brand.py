from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CarWaleBrand(BaseModel):
    """
    MongoDB representation of one CarWale brand.

    The complete CarWale brand response is retained in
    `data`, while commonly queried identity fields are
    also stored at the top level.

    MongoDB stores the raw brand fields in flattened form.
    When reading a document, `data` is reconstructed from
    those flattened fields.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    document_id: str = Field(
        alias="_id",
        min_length=1,
    )

    make_id: int = Field(
        alias="makeId",
        gt=0,
    )

    make_name: str = Field(
        alias="makeName",
        min_length=1,
    )

    masking_name: str = Field(
        alias="maskingName",
        min_length=1,
    )

    data: dict[str, Any]

    last_run_id: str = Field(
        alias="lastRunId",
        min_length=1,
    )

    scraped_at: datetime = Field(
        alias="scrapedAt",
    )

    created_at: datetime = Field(
        alias="createdAt",
    )

    updated_at: datetime = Field(
        alias="updatedAt",
    )

    @model_validator(mode="before")
    @classmethod
    def restore_data(
        cls,
        values: Any,
    ) -> Any:
        """
        Rebuild the raw `data` object when loading a flattened
        MongoDB document.

        The repository intentionally stores raw CarWale fields
        at the document's top level, so MongoDB documents do not
        contain a nested `data` field.
        """
        if not isinstance(values, Mapping):
            return values

        document = dict(values)

        if "data" in document:
            return document

        protected_fields = {
            "_id",
            "lastRunId",
            "scrapedAt",
            "createdAt",
            "updatedAt",
        }

        document["data"] = {
            key: value for key, value in document.items() if key not in protected_fields
        }

        return document

    @staticmethod
    def build_document_id(
        make_id: int,
    ) -> str:
        if isinstance(make_id, bool) or not isinstance(make_id, int) or make_id <= 0:
            raise ValueError("make_id must be a positive integer")

        return f"make:{make_id}"

    @classmethod
    def create(
        cls,
        *,
        brand: Mapping[str, Any],
        run_id: str,
        created_at: datetime | None = None,
    ) -> Self:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        make_id = brand.get("makeId")

        make_name = brand.get("makeName")

        masking_name = brand.get("maskingName")

        if isinstance(make_id, bool) or not isinstance(make_id, int) or make_id <= 0:
            raise ValueError("Brand makeId must be a positive integer")

        if not isinstance(
            make_name,
            str,
        ):
            raise ValueError("Brand makeName must be a string")

        normalized_make_name = make_name.strip()

        if not normalized_make_name:
            raise ValueError("Brand makeName cannot be empty")

        if not isinstance(
            masking_name,
            str,
        ):
            raise ValueError("Brand maskingName must be a string")

        normalized_masking_name = masking_name.strip().lower()

        if not normalized_masking_name:
            raise ValueError("Brand maskingName cannot be empty")

        if not MASKING_NAME_PATTERN.fullmatch(normalized_masking_name):
            raise ValueError(
                "Brand maskingName contains invalid "
                "characters: "
                f"{normalized_masking_name!r}"
            )

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        raw_data = dict(brand)

        raw_data["makeId"] = make_id
        raw_data["makeName"] = normalized_make_name
        raw_data["maskingName"] = normalized_masking_name

        return cls(
            _id=cls.build_document_id(make_id),
            makeId=make_id,
            makeName=normalized_make_name,
            maskingName=normalized_masking_name,
            data=raw_data,
            lastRunId=normalized_run_id,
            scrapedAt=current_time,
            createdAt=initial_created_at,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        document = self.model_dump(
            by_alias=True,
            mode="python",
        )

        raw_data = document.pop("data")

        protected_fields = {
            "_id",
            "lastRunId",
            "scrapedAt",
            "createdAt",
            "updatedAt",
        }

        for key, value in raw_data.items():
            if key in protected_fields:
                continue

            document[key] = value

        return document
