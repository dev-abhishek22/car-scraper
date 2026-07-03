from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

BrandStatus = Literal[
    "CURRENT",
    "UPCOMING",
    "EXPIRED",
]


class CarDekhoBrand(BaseModel):
    """
    MongoDB representation of one CarDekho brand.

    The document ID is generated from the brand slug
    because upcoming and expired brands may not have
    a numeric CarDekho brand ID.

    Selected brand fields are stored in flattened form
    in MongoDB.
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

    brand_id: int | None = Field(
        default=None,
        alias="id",
        gt=0,
    )

    brand_name: str = Field(
        alias="brandName",
        min_length=1,
    )

    slug: str = Field(
        min_length=1,
    )

    model_request_slug: str = Field(
        alias="modelRequestSlug",
        min_length=1,
    )

    brand_status: BrandStatus = Field(
        alias="brandStatus",
    )

    is_current: bool = Field(
        alias="isCurrent",
    )

    is_upcoming: bool = Field(
        alias="isUpcoming",
    )

    is_expired: bool = Field(
        alias="isExpired",
    )

    brand_url: str = Field(
        alias="brandUrl",
        min_length=1,
    )

    tool_tip_text: str | None = Field(
        default=None,
        alias="toolTipText",
    )

    image: str | None = None

    is_popular: int | None = Field(
        default=None,
        alias="isPopular",
        ge=0,
        le=1,
    )

    popularity: int | None = Field(
        default=None,
        ge=0,
    )

    total_offer_count: int | None = Field(
        default=None,
        alias="totalOfferCount",
        ge=0,
    )

    offer_url: str | None = Field(
        default=None,
        alias="offerUrl",
    )

    has_offer_data: bool = Field(
        alias="hasOfferData",
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
        Rebuild the `data` field when loading a flattened
        MongoDB document.
        """
        if not isinstance(
            values,
            Mapping,
        ):
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

    @model_validator(mode="after")
    def validate_status_flags(
        self,
    ) -> Self:
        expected_flags = {
            "CURRENT": (
                True,
                False,
                False,
            ),
            "UPCOMING": (
                False,
                True,
                False,
            ),
            "EXPIRED": (
                False,
                False,
                True,
            ),
        }

        expected = expected_flags[self.brand_status]

        actual = (
            self.is_current,
            self.is_upcoming,
            self.is_expired,
        )

        if actual != expected:
            raise ValueError(
                "Brand status flags do not match " f"brandStatus={self.brand_status!r}"
            )

        return self

    @staticmethod
    def _normalize_slug(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError(f"Brand {field_name} must be a string")

        normalized_value = value.strip().lower().replace("_", "-").replace(" ", "-")

        normalized_value = re.sub(
            r"-+",
            "-",
            normalized_value,
        ).strip("-")

        if not normalized_value:
            raise ValueError(f"Brand {field_name} cannot be empty")

        if not SLUG_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"Brand {field_name} contains invalid "
                f"characters: {normalized_value!r}"
            )

        return normalized_value

    @staticmethod
    def _normalize_required_string(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError(f"Brand {field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"Brand {field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _normalize_optional_string(
        value: Any,
        *,
        field_name: str,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(
            value,
            str,
        ):
            raise ValueError(f"Brand {field_name} must be a string " "or null")

        normalized_value = value.strip()

        return normalized_value or None

    @staticmethod
    def _normalize_optional_positive_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int | None:
        if value is None:
            return None

        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(
                f"Brand {field_name} must be a " "positive integer or null"
            )

        return value

    @staticmethod
    def _normalize_optional_non_negative_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int | None:
        if value is None:
            return None

        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(
                f"Brand {field_name} must be a " "non-negative integer or null"
            )

        return value

    @staticmethod
    def _normalize_boolean(
        value: Any,
        *,
        field_name: str,
    ) -> bool:
        if not isinstance(
            value,
            bool,
        ):
            raise ValueError(f"Brand {field_name} must be a boolean")

        return value

    @staticmethod
    def _normalize_brand_status(
        value: Any,
    ) -> BrandStatus:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError("Brand brandStatus must be a string")

        normalized_status = value.strip().upper()

        if normalized_status not in {
            "CURRENT",
            "UPCOMING",
            "EXPIRED",
        }:
            raise ValueError(
                "Brand brandStatus must be one of: " "CURRENT, UPCOMING, EXPIRED"
            )

        return normalized_status  # type: ignore[return-value]

    @staticmethod
    def _build_status_flags(
        brand_status: BrandStatus,
    ) -> dict[str, bool]:
        return {
            "isCurrent": (brand_status == "CURRENT"),
            "isUpcoming": (brand_status == "UPCOMING"),
            "isExpired": (brand_status == "EXPIRED"),
        }

    @classmethod
    def build_document_id(
        cls,
        slug: str,
    ) -> str:
        normalized_slug = cls._normalize_slug(
            slug,
            field_name="slug",
        )

        return f"brand:{normalized_slug}"

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

        brand_id = cls._normalize_optional_positive_integer(
            brand.get("id"),
            field_name="id",
        )

        brand_name = cls._normalize_required_string(
            brand.get("brandName"),
            field_name="brandName",
        )

        slug = cls._normalize_slug(
            brand.get("slug"),
            field_name="slug",
        )

        model_request_slug = cls._normalize_slug(
            brand.get("modelRequestSlug"),
            field_name="modelRequestSlug",
        )

        brand_status = cls._normalize_brand_status(brand.get("brandStatus"))

        status_flags = cls._build_status_flags(brand_status)

        provided_is_current = cls._normalize_boolean(
            brand.get("isCurrent"),
            field_name="isCurrent",
        )

        provided_is_upcoming = cls._normalize_boolean(
            brand.get("isUpcoming"),
            field_name="isUpcoming",
        )

        provided_is_expired = cls._normalize_boolean(
            brand.get("isExpired"),
            field_name="isExpired",
        )

        provided_flags = {
            "isCurrent": provided_is_current,
            "isUpcoming": provided_is_upcoming,
            "isExpired": provided_is_expired,
        }

        if provided_flags != status_flags:
            raise ValueError(
                "Brand status flags do not match " f"brandStatus={brand_status!r}"
            )

        brand_url = cls._normalize_required_string(
            brand.get("brandUrl"),
            field_name="brandUrl",
        )

        tool_tip_text = cls._normalize_optional_string(
            brand.get("toolTipText"),
            field_name="toolTipText",
        )

        image = cls._normalize_optional_string(
            brand.get("image"),
            field_name="image",
        )

        is_popular = cls._normalize_optional_non_negative_integer(
            brand.get("isPopular"),
            field_name="isPopular",
        )

        if is_popular not in {
            None,
            0,
            1,
        }:
            raise ValueError("Brand isPopular must be 0, 1, or null")

        popularity = cls._normalize_optional_non_negative_integer(
            brand.get("popularity"),
            field_name="popularity",
        )

        total_offer_count = cls._normalize_optional_non_negative_integer(
            brand.get("totalOfferCount"),
            field_name="totalOfferCount",
        )

        offer_url = cls._normalize_optional_string(
            brand.get("offerUrl"),
            field_name="offerUrl",
        )

        has_offer_data = cls._normalize_boolean(
            brand.get("hasOfferData"),
            field_name="hasOfferData",
        )

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        raw_data: dict[str, Any] = {
            "id": brand_id,
            "brandName": brand_name,
            "slug": slug,
            "modelRequestSlug": (model_request_slug),
            "brandStatus": brand_status,
            **status_flags,
            "brandUrl": brand_url,
            "toolTipText": tool_tip_text,
            "image": image,
            "isPopular": is_popular,
            "popularity": popularity,
            "totalOfferCount": (total_offer_count),
            "offerUrl": offer_url,
            "hasOfferData": has_offer_data,
        }

        return cls(
            _id=cls.build_document_id(slug),
            id=brand_id,
            brandName=brand_name,
            slug=slug,
            modelRequestSlug=model_request_slug,
            brandStatus=brand_status,
            **status_flags,
            brandUrl=brand_url,
            toolTipText=tool_tip_text,
            image=image,
            isPopular=is_popular,
            popularity=popularity,
            totalOfferCount=total_offer_count,
            offerUrl=offer_url,
            hasOfferData=has_offer_data,
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
