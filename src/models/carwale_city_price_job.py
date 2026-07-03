from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

MASKING_NAME_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"


class CarWaleCityPriceJob(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    version_id: int = Field(
        gt=0,
    )

    city_id: int = Field(
        gt=0,
    )

    make_masking_name: str = Field(
        min_length=1,
        pattern=MASKING_NAME_PATTERN,
    )

    model_masking_name: str = Field(
        min_length=1,
        pattern=MASKING_NAME_PATTERN,
    )

    city_masking_name: str = Field(
        min_length=1,
        pattern=MASKING_NAME_PATTERN,
    )

    @property
    def item_key(self) -> str:
        """
        Permanent identifier for one version-city combination.

        This same value is used as the MongoDB document _id
        for successful city-price records.
        """
        return f"v:{self.version_id}:c:{self.city_id}"
