from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any

from src.clients.async_client import AsyncExternalHttpClient
from src.clients.client import ExternalResponseError
from src.external.constants.cardekho import (
    CARDEKHO_BASE_URL,
    CARDEKHO_MODEL_PRICE,
)
from src.models.cardekho_city_price import (
    CardekhoCityPrice,
    CardekhoCityPriceAccessoryItem,
    CardekhoCityPriceAmounts,
    CardekhoCityPriceDifference,
    CardekhoCityPriceDisplayPrices,
    CardekhoCityPriceEmi,
    CardekhoCityPriceOptionalAccessories,
    CardekhoCityPriceOtherChargeItem,
    CardekhoCityPriceOtherCharges,
    CardekhoCityPriceRange,
    CardekhoCityPriceRequest,
    CardekhoCityPriceSource,
    CardekhoCityPriceVariant,
    CardekhoCityPriceVariantStats,
)
from src.models.cardekho_city_price_job import (
    CardekhoCityPriceJob,
    CardekhoCityPriceSourceTrim,
)

PRICE_NUMBER_PATTERN = re.compile(r"-?\d[\d,]*(?:\.\d+)?")

PERCENT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*%")

YEAR_PATTERN = re.compile(
    r"(\d+)\s*years?",
    re.IGNORECASE,
)

MONTH_PATTERN = re.compile(
    r"(\d+)\s*months?",
    re.IGNORECASE,
)

MULTIPLE_SPACES_PATTERN = re.compile(r"\s+")

PRICE_EXTRA_KEYWORDS = (
    "price",
    "amount",
    "charge",
    "fee",
    "tax",
    "rto",
    "insurance",
    "accessor",
    "emi",
    "loan",
    "downpayment",
    "payable",
    "interest",
)

EXCLUDED_ADDITIONAL_PRICE_FIELDS = {
    "exShowRoom",
    "rto",
    "insurance",
    "others",
    "optionalAccessories",
    "ORPWithoutOptionAccessories",
    "ORPWithoutOptionAccessoriesDoubleType",
    "onRoadPriceInIndianFormat",
    "onRoadPriceOfVariant",
    "priceType",
    "threeDigitExShowRoomPrice",
    "emi",
    "threeDigitOnROadPrice",
    "priceUrl",
    "threeDigitOnRoadWithoutOptional",
    "variantSlug",
    "differentiatePrice",
    "emiBreakup",
    "financeDto",
    "insuranceViewAllDto",
    "priceBreakupAiEntryPoint",
    "smartEmiPlannerAiEntryPoint",
    "emiCalculatorText",
    "emiCalculatorUrl",
    "applicableForloEMI",
    "loEMI",
}


class CardekhoCityPriceExecutor:
    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self._client = client

    @staticmethod
    def _optional_string(
        value: Any,
    ) -> str | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        normalized = value.strip()

        return normalized or None

    @staticmethod
    def _positive_integer(
        value: Any,
    ) -> int | None:
        if isinstance(
            value,
            bool,
        ):
            return None

        if isinstance(
            value,
            int,
        ):
            return value if value > 0 else None

        if (
            isinstance(
                value,
                str,
            )
            and value.strip().isdigit()
        ):
            parsed = int(value.strip())

            return parsed if parsed > 0 else None

        return None

    @staticmethod
    def _optional_bool(
        value: Any,
    ) -> bool | None:
        if isinstance(
            value,
            bool,
        ):
            return value

        if (
            isinstance(
                value,
                int,
            )
            and not isinstance(
                value,
                bool,
            )
            and value
            in {
                0,
                1,
            }
        ):
            return value == 1

        if isinstance(
            value,
            str,
        ):
            normalized = value.strip().lower()

            if normalized in {
                "true",
                "1",
                "yes",
            }:
                return True

            if normalized in {
                "false",
                "0",
                "no",
            }:
                return False

        return None

    @classmethod
    def _as_bool(
        cls,
        value: Any,
        *,
        default: bool = False,
    ) -> bool:
        parsed = cls._optional_bool(value)

        return parsed if parsed is not None else default

    @staticmethod
    def _slugify(
        value: str,
    ) -> str:
        normalized = unicodedata.normalize(
            "NFKD",
            value,
        )

        ascii_value = normalized.encode(
            "ascii",
            "ignore",
        ).decode("ascii")

        slug = re.sub(
            r"[^a-zA-Z0-9]+",
            "-",
            ascii_value,
        ).lower()

        return re.sub(
            r"-+",
            "-",
            slug,
        ).strip("-")

    @classmethod
    def _normalize_slug(
        cls,
        value: Any,
    ) -> str | None:
        normalized = cls._optional_string(value)

        if normalized is None:
            return None

        slug = cls._slugify(normalized)

        return slug or None

    @classmethod
    def _normalize_name(
        cls,
        value: Any,
    ) -> str | None:
        normalized = cls._optional_string(value)

        if normalized is None:
            return None

        return MULTIPLE_SPACES_PATTERN.sub(
            " ",
            normalized.casefold(),
        )

    @classmethod
    def _normalize_url(
        cls,
        value: Any,
    ) -> str | None:
        normalized = cls._optional_string(value)

        if normalized is None:
            return None

        normalized = normalized.split(
            "?",
            1,
        )[0].strip()

        if not normalized.startswith("/"):
            normalized = f"/{normalized}"

        return normalized.rstrip("/").casefold()

    @staticmethod
    def _currency_amount(
        value: Any,
    ) -> int | None:
        if value is None or isinstance(
            value,
            bool,
        ):
            return None

        if isinstance(
            value,
            int,
        ):
            return value if value >= 0 else None

        if isinstance(
            value,
            float,
        ):
            return round(value) if value >= 0 else None

        if not isinstance(
            value,
            str,
        ):
            return None

        normalized = value.strip().lower()

        match = PRICE_NUMBER_PATTERN.search(normalized)

        if match is None:
            return None

        try:
            number = float(
                match.group(0).replace(
                    ",",
                    "",
                )
            )

        except ValueError:
            return None

        multiplier = 1.0

        if "crore" in normalized or " cr" in f" {normalized}":
            multiplier = 10_000_000.0

        elif "lakh" in normalized or " lac" in f" {normalized}":
            multiplier = 100_000.0

        elif "thousand" in normalized:
            multiplier = 1_000.0

        parsed = round(number * multiplier)

        return parsed if parsed >= 0 else None

    @staticmethod
    def _percentage(
        value: Any,
    ) -> float | None:
        if value is None or isinstance(
            value,
            bool,
        ):
            return None

        if isinstance(
            value,
            (
                int,
                float,
            ),
        ):
            return float(value) if value >= 0 else None

        if not isinstance(
            value,
            str,
        ):
            return None

        match = PERCENT_PATTERN.search(value)

        if match is None:
            return None

        try:
            return float(match.group(1))

        except ValueError:
            return None

    @staticmethod
    def _tenure_months(
        value: Any,
    ) -> int | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        year_match = YEAR_PATTERN.search(value)

        if year_match is not None:
            return int(year_match.group(1)) * 12

        month_match = MONTH_PATTERN.search(value)

        if month_match is not None:
            return int(month_match.group(1))

        return None

    @classmethod
    def _split_values(
        cls,
        value: Any,
    ) -> list[str]:
        normalized = cls._optional_string(value)

        if normalized is None:
            return []

        values: list[str] = []
        seen: set[str] = set()

        for item in re.split(
            r"[/,|]",
            normalized,
        ):
            item = MULTIPLE_SPACES_PATTERN.sub(
                " ",
                item.strip(),
            )

            key = item.casefold()

            if not item or key in seen:
                continue

            seen.add(key)

            values.append(item)

        return values

    @classmethod
    def _find_price_detail(
        cls,
        data: Mapping[
            str,
            Any,
        ],
        *,
        job: CardekhoCityPriceJob,
    ) -> dict[str, Any]:
        raw_sections = data.get("priceDetailSection")

        if not isinstance(
            raw_sections,
            list,
        ):
            raise ExternalResponseError(
                "CarDekho model-price "
                "response does not contain "
                "a valid priceDetailSection "
                "array"
            )

        expected_url = cls._normalize_url(f"/{job.brand_slug}/{job.model_slug}")

        expected_brand = cls._normalize_name(job.brand_name)

        fallback: dict[str, Any] | None = None

        for raw_section in raw_sections:
            if not isinstance(
                raw_section,
                Mapping,
            ):
                continue

            section = dict(raw_section)

            section_id = cls._positive_integer(section.get("id"))

            dcb_dto = section.get("dcbDto")

            dcb_model_id: int | None = None

            dcb_model_slug: str | None = None

            if isinstance(
                dcb_dto,
                Mapping,
            ):
                dcb_model_id = cls._positive_integer(dcb_dto.get("modelId"))

                dcb_model_slug = cls._normalize_slug(dcb_dto.get("modelSlug"))

            if section_id == job.model_id or dcb_model_id == job.model_id:
                return section

            section_url = cls._normalize_url(section.get("modelUrl"))

            section_brand = cls._normalize_name(section.get("brandName"))

            if section_url == expected_url:
                fallback = section

            elif dcb_model_slug == job.model_slug and section_brand == expected_brand:
                fallback = section

        if fallback is not None:
            return fallback

        raise ExternalResponseError(
            "CarDekho model-price response "
            "does not contain the requested "
            "model: "
            f"model_id={job.model_id}, "
            "model_slug="
            f"{job.model_slug!r}"
        )

    @classmethod
    def _optional_accessories(
        cls,
        value: Any,
    ) -> CardekhoCityPriceOptionalAccessories | None:
        if not isinstance(
            value,
            Mapping,
        ):
            return None

        total = cls._currency_amount(value.get("totalAccessories"))

        if total is None:
            total = cls._currency_amount(value.get("totalAccessoriesInRs"))

        total_display = cls._optional_string(
            value.get("totalAccessoriesInRs")
        ) or cls._optional_string(value.get("totalAccessoriesInRsFormat"))

        items: list[CardekhoCityPriceAccessoryItem] = []

        raw_items = value.get("list")

        if isinstance(
            raw_items,
            list,
        ):
            for raw_item in raw_items:
                if not isinstance(
                    raw_item,
                    Mapping,
                ):
                    continue

                name = cls._optional_string(raw_item.get("text"))

                amount = cls._currency_amount(raw_item.get("value"))

                if amount is None:
                    amount = cls._currency_amount(raw_item.get("price"))

                if name is None or amount is None:
                    continue

                items.append(
                    CardekhoCityPriceAccessoryItem(
                        key=(cls._optional_string(raw_item.get("key"))),
                        name=name,
                        amount=amount,
                        display=(cls._optional_string(raw_item.get("price"))),
                    )
                )

        if total is None:
            total = sum(item.amount for item in items)

        return CardekhoCityPriceOptionalAccessories(
            total=total,
            totalDisplay=total_display,
            items=items,
        )

    @classmethod
    def _other_charges(
        cls,
        value: Any,
    ) -> CardekhoCityPriceOtherCharges | None:
        if not isinstance(
            value,
            Mapping,
        ):
            return None

        total = cls._currency_amount(value.get("totalOtherCharges"))

        if total is None:
            total = cls._currency_amount(value.get("totalOtherChargesInRsFormat"))

        total_display = cls._optional_string(value.get("totalOtherChargesInRsFormat"))

        items: list[CardekhoCityPriceOtherChargeItem] = []

        raw_items = value.get("list")

        if isinstance(
            raw_items,
            list,
        ):
            for raw_item in raw_items:
                if not isinstance(
                    raw_item,
                    Mapping,
                ):
                    continue

                name = cls._optional_string(raw_item.get("text"))

                amount = cls._currency_amount(raw_item.get("value"))

                if amount is None:
                    amount = cls._currency_amount(raw_item.get("price"))

                if name is None or amount is None:
                    continue

                items.append(
                    CardekhoCityPriceOtherChargeItem(
                        key=(cls._optional_string(raw_item.get("key"))),
                        name=name,
                        amount=amount,
                        display=(cls._optional_string(raw_item.get("price"))),
                    )
                )

        if total is None:
            total = sum(item.amount for item in items)

        if total == 0 and not items and total_display is None:
            return None

        return CardekhoCityPriceOtherCharges(
            total=total,
            totalDisplay=total_display,
            items=items,
        )

    @classmethod
    def _difference(
        cls,
        value: Any,
    ) -> CardekhoCityPriceDifference | None:
        display = cls._optional_string(value)

        if display is None:
            return None

        return CardekhoCityPriceDifference(
            amount=(cls._currency_amount(display)),
            display=display,
        )

    @classmethod
    def _emi(
        cls,
        raw_variant: Mapping[
            str,
            Any,
        ],
    ) -> CardekhoCityPriceEmi | None:
        monthly = cls._currency_amount(raw_variant.get("emi"))

        low_emi_applicable = cls._optional_bool(raw_variant.get("applicableForloEMI"))

        low_monthly_amount = cls._currency_amount(raw_variant.get("loEMI"))

        interest_rate: float | None = None

        tenure_months: int | None = None

        values: dict[
            str,
            int,
        ] = {}

        raw_breakup = raw_variant.get("emiBreakup")

        if isinstance(
            raw_breakup,
            Mapping,
        ):
            breakup_monthly = cls._currency_amount(raw_breakup.get("emi"))

            if breakup_monthly is not None:
                monthly = breakup_monthly

            interest_text = raw_breakup.get("interstrateText") or raw_breakup.get(
                "interestRateText"
            )

            interest_rate = cls._percentage(interest_text)

            tenure_months = cls._tenure_months(interest_text)

            raw_items = raw_breakup.get("items")

            if isinstance(
                raw_items,
                list,
            ):
                for raw_item in raw_items:
                    if not isinstance(
                        raw_item,
                        Mapping,
                    ):
                        continue

                    slug = cls._normalize_slug(raw_item.get("slug"))

                    amount = cls._currency_amount(raw_item.get("value"))

                    if amount is None:
                        amount = cls._currency_amount(raw_item.get("price"))

                    if slug is not None and amount is not None:
                        values[slug] = amount

        fields = (
            monthly,
            low_emi_applicable,
            low_monthly_amount,
            interest_rate,
            tenure_months,
            values.get("down-payment"),
            values.get("loan-amount"),
            values.get("interest-amount"),
            values.get("payable-amount"),
        )

        if all(value is None for value in fields):
            return None

        return CardekhoCityPriceEmi(
            monthlyAmount=monthly,
            lowEmiApplicable=(low_emi_applicable),
            lowMonthlyAmount=(low_monthly_amount),
            interestRate=interest_rate,
            tenureMonths=tenure_months,
            downPayment=values.get("down-payment"),
            loanAmount=values.get("loan-amount"),
            interestAmount=values.get("interest-amount"),
            payableAmount=values.get("payable-amount"),
        )

    @staticmethod
    def _additional_price_data(
        raw_variant: Mapping[
            str,
            Any,
        ],
    ) -> dict[str, Any]:
        result: dict[
            str,
            Any,
        ] = {}

        for (
            key,
            value,
        ) in raw_variant.items():
            if key in EXCLUDED_ADDITIONAL_PRICE_FIELDS:
                continue

            normalized_key = (
                key.casefold()
                .replace(
                    "-",
                    "",
                )
                .replace(
                    "_",
                    "",
                )
            )

            if not any(keyword in normalized_key for keyword in PRICE_EXTRA_KEYWORDS):
                continue

            if isinstance(
                value,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            ):
                result[key] = value

        return result

    @classmethod
    def _trim_indexes(
        cls,
        source_trims: Sequence[CardekhoCityPriceSourceTrim],
    ) -> tuple[
        dict[
            str,
            CardekhoCityPriceSourceTrim,
        ],
        dict[
            str,
            CardekhoCityPriceSourceTrim,
        ],
        dict[
            str,
            CardekhoCityPriceSourceTrim,
        ],
    ]:
        by_slug: dict[
            str,
            CardekhoCityPriceSourceTrim,
        ] = {}

        by_url: dict[
            str,
            CardekhoCityPriceSourceTrim,
        ] = {}

        by_name: dict[
            str,
            CardekhoCityPriceSourceTrim,
        ] = {}

        for trim in source_trims:
            by_slug.setdefault(
                trim.slug,
                trim,
            )

            normalized_url = cls._normalize_url(trim.url)

            normalized_name = cls._normalize_name(trim.name)

            normalized_short_name = cls._normalize_name(trim.short_name)

            if normalized_url is not None:
                by_url.setdefault(
                    normalized_url,
                    trim,
                )

            if normalized_name is not None:
                by_name.setdefault(
                    normalized_name,
                    trim,
                )

            if normalized_short_name is not None:
                by_name.setdefault(
                    normalized_short_name,
                    trim,
                )

        return (
            by_slug,
            by_url,
            by_name,
        )

    @classmethod
    def _match_trim(
        cls,
        raw_variant: Mapping[
            str,
            Any,
        ],
        *,
        by_slug: Mapping[
            str,
            CardekhoCityPriceSourceTrim,
        ],
        by_url: Mapping[
            str,
            CardekhoCityPriceSourceTrim,
        ],
        by_name: Mapping[
            str,
            CardekhoCityPriceSourceTrim,
        ],
    ) -> CardekhoCityPriceSourceTrim | None:
        slug = cls._normalize_slug(raw_variant.get("variantSlug"))

        if slug is not None and slug in by_slug:
            return by_slug[slug]

        url = cls._normalize_url(raw_variant.get("variantUrl"))

        if url is not None and url in by_url:
            return by_url[url]

        for field_name in (
            "variantDisplayName",
            "variantId",
            "variantDisplayId",
            "variantShortName",
        ):
            name = cls._normalize_name(raw_variant.get(field_name))

            if name is not None and name in by_name:
                return by_name[name]

        return None

    @classmethod
    def _variant(
        cls,
        raw_variant: Mapping[
            str,
            Any,
        ],
        *,
        source_trim: CardekhoCityPriceSourceTrim | None,
    ) -> CardekhoCityPriceVariant:
        api_name = (
            cls._optional_string(raw_variant.get("variantDisplayName"))
            or cls._optional_string(raw_variant.get("variantId"))
            or cls._optional_string(raw_variant.get("variantDisplayId"))
        )

        if api_name is None:
            raise ExternalResponseError(
                "CarDekho price variant does not contain a valid variant name"
            )

        api_slug = cls._normalize_slug(raw_variant.get("variantSlug"))

        if api_slug is None:
            api_slug = cls._slugify(api_name)

        variant_url = cls._optional_string(raw_variant.get("variantUrl"))

        if variant_url is not None and not variant_url.startswith("/"):
            variant_url = f"/{variant_url}"

        on_road_without_optional = cls._currency_amount(
            raw_variant.get("ORPWithoutOptionAccessoriesDoubleType")
        )

        if on_road_without_optional is None:
            on_road_without_optional = cls._currency_amount(
                raw_variant.get("ORPWithoutOptionAccessories")
            )

        on_road = cls._currency_amount(raw_variant.get("onRoadPriceOfVariant"))

        if on_road is None:
            on_road = cls._currency_amount(raw_variant.get("onRoadPriceInIndianFormat"))

        prices = CardekhoCityPriceAmounts(
            exShowroom=(cls._currency_amount(raw_variant.get("exShowRoom"))),
            rto=(cls._currency_amount(raw_variant.get("rto"))),
            insurance=(cls._currency_amount(raw_variant.get("insurance"))),
            optionalAccessories=(
                cls._optional_accessories(raw_variant.get("optionalAccessories"))
            ),
            otherCharges=(cls._other_charges(raw_variant.get("others"))),
            onRoadWithoutOptionalAccessories=(on_road_without_optional),
            onRoad=on_road,
            differenceToNextVariant=(
                cls._difference(raw_variant.get("differentiatePrice"))
            ),
            additionalPriceData=(cls._additional_price_data(raw_variant)),
        )

        display_prices = CardekhoCityPriceDisplayPrices(
            exShowroom=(
                cls._optional_string(raw_variant.get("threeDigitExShowRoomPrice"))
            ),
            onRoad=(cls._optional_string(raw_variant.get("threeDigitOnROadPrice"))),
            onRoadWithoutOptionalAccessories=(
                cls._optional_string(raw_variant.get("threeDigitOnRoadWithoutOptional"))
            ),
        )

        if all(
            value is None
            for value in (
                display_prices.ex_showroom,
                display_prices.on_road,
                (display_prices.on_road_without_optional_accessories),
            )
        ):
            display_prices_value = None

        else:
            display_prices_value = display_prices

        return CardekhoCityPriceVariant(
            trimId=(source_trim.trim_id if source_trim else None),
            trimName=(source_trim.name if source_trim else None),
            trimShortName=(source_trim.short_name if source_trim else None),
            trimSlug=(source_trim.slug if source_trim else None),
            trimStatus=(source_trim.status if source_trim else None),
            trimUrl=(source_trim.url if source_trim else None),
            apiVariantName=api_name,
            apiVariantSlug=api_slug,
            variantDisplayName=(
                cls._optional_string(raw_variant.get("variantDisplayName"))
            ),
            variantDisplayId=(
                cls._optional_string(raw_variant.get("variantDisplayId"))
            ),
            fuelType=(cls._optional_string(raw_variant.get("variantFuelType"))),
            priceType=(cls._optional_string(raw_variant.get("priceType"))),
            prices=prices,
            emi=cls._emi(raw_variant),
            displayPrices=(display_prices_value),
            variantSlug=api_slug,
            variantUrl=variant_url,
            priceUrl=(cls._optional_string(raw_variant.get("priceUrl"))),
            tag=(cls._optional_string(raw_variant.get("tag"))),
            topSelling=(cls._as_bool(raw_variant.get("topSelling"))),
            isRecentLaunch=(cls._as_bool(raw_variant.get("isRecentLaunch"))),
        )

    @classmethod
    def _variants(
        cls,
        price_detail: Mapping[
            str,
            Any,
        ],
        *,
        job: CardekhoCityPriceJob,
        price_available: bool,
    ) -> tuple[
        list[CardekhoCityPriceVariant],
        CardekhoCityPriceVariantStats,
    ]:
        raw_detail = price_detail.get("variantDetailByFuel")

        if not isinstance(
            raw_detail,
            Mapping,
        ):
            if not price_available:
                return (
                    [],
                    CardekhoCityPriceVariantStats(
                        apiVariants=0,
                        storedVariants=0,
                        matchedWithSourceTrims=0,
                        unmatchedSourceTrims=len(job.source_trims),
                        unmatchedApiVariants=0,
                    ),
                )

            raise ExternalResponseError(
                "CarDekho price detail does "
                "not contain a valid "
                "variantDetailByFuel object"
            )

        raw_variants = raw_detail.get("variantList")

        if not isinstance(
            raw_variants,
            list,
        ):
            if not price_available:
                raw_variants = []

            else:
                raise ExternalResponseError(
                    "CarDekho "
                    "variantDetailByFuel "
                    "does not contain a valid "
                    "variantList array"
                )

        (
            by_slug,
            by_url,
            by_name,
        ) = cls._trim_indexes(job.source_trims)

        variants: list[CardekhoCityPriceVariant] = []

        matched_trim_ids: set[int] = set()

        matched_api_variants = 0
        api_variants = 0

        for raw_variant in raw_variants:
            if not isinstance(
                raw_variant,
                Mapping,
            ):
                continue

            api_variants += 1

            source_trim = cls._match_trim(
                raw_variant,
                by_slug=by_slug,
                by_url=by_url,
                by_name=by_name,
            )

            variants.append(
                cls._variant(
                    raw_variant,
                    source_trim=(source_trim),
                )
            )

            if source_trim is not None:
                matched_api_variants += 1

                matched_trim_ids.add(source_trim.trim_id)

        if price_available and not variants:
            raise ExternalResponseError(
                "CarDekho returned an "
                "available model price "
                "without usable variants: "
                f"model_id={job.model_id}, "
                f"city_id={job.city_id}"
            )

        return (
            variants,
            CardekhoCityPriceVariantStats(
                apiVariants=(api_variants),
                storedVariants=len(variants),
                matchedWithSourceTrims=(matched_api_variants),
                unmatchedSourceTrims=max(
                    (len(job.source_trims) - len(matched_trim_ids)),
                    0,
                ),
                unmatchedApiVariants=max(
                    (len(variants) - matched_api_variants),
                    0,
                ),
            ),
        )

    @classmethod
    def _price_range(
        cls,
        price_detail: Mapping[
            str,
            Any,
        ],
        *,
        variants: Sequence[CardekhoCityPriceVariant],
    ) -> CardekhoCityPriceRange | None:
        minimum = cls._currency_amount(price_detail.get("minPrice"))

        maximum = cls._currency_amount(price_detail.get("maxPrice"))

        ex_showroom_prices = [
            variant.prices.ex_showroom
            for variant in variants
            if (variant.prices.ex_showroom is not None)
        ]

        if minimum is None and ex_showroom_prices:
            minimum = min(ex_showroom_prices)

        if maximum is None and ex_showroom_prices:
            maximum = max(ex_showroom_prices)

        display = cls._optional_string(price_detail.get("priceRange"))

        if display is None and minimum is None and maximum is None:
            return None

        return CardekhoCityPriceRange(
            display=display,
            minimumExShowroom=minimum,
            maximumExShowroom=maximum,
        )

    @classmethod
    def _fuel_types(
        cls,
        price_detail: Mapping[
            str,
            Any,
        ],
        *,
        variants: Sequence[CardekhoCityPriceVariant],
    ) -> list[str]:
        values = cls._split_values(price_detail.get("fuelType"))

        seen = {value.casefold() for value in values}

        for variant in variants:
            if variant.fuel_type is None:
                continue

            key = variant.fuel_type.casefold()

            if key in seen:
                continue

            seen.add(key)

            values.append(variant.fuel_type)

        return values

    @classmethod
    def _redirect_url(
        cls,
        data: Mapping[
            str,
            Any,
        ],
    ) -> str | None:
        redirect = data.get("redirect")

        if not isinstance(
            redirect,
            Mapping,
        ):
            return None

        redirect_status_code = cls._positive_integer(redirect.get("statusCode"))

        redirect_url = cls._optional_string(redirect.get("redirectURL"))

        if redirect_url is None:
            return None

        if redirect_status_code is not None and not 300 <= redirect_status_code <= 399:
            return None

        if not redirect_url.startswith("/"):
            redirect_url = f"/{redirect_url}"

        return redirect_url

    @classmethod
    def _unavailable_record(
        cls,
        *,
        job: CardekhoCityPriceJob,
    ) -> CardekhoCityPrice:
        return CardekhoCityPrice(
            modelId=job.model_id,
            modelName=job.model_name,
            modelSlug=job.model_slug,
            modelStatus=job.model_status,
            brandId=job.brand_id,
            brandName=job.brand_name,
            brandSlug=job.brand_slug,
            carSlug=job.car_slug,
            cityId=job.city_id,
            cityName=job.city_name,
            cityDisplayName=(job.city_display_name),
            citySlug=job.city_slug,
            isPopularCity=(job.is_popular_city),
            priceAvailable=False,
            priceRange=None,
            priceDetailTitle=None,
            modelUrl=(f"/{job.brand_slug}/{job.model_slug}"),
            priceUrl=(f"/{job.request_url_value}"),
            estimatedText=None,
            fuelTypes=[],
            transmissionTypes=[],
            totalVariants=0,
            variants=[],
            variantStats=(
                CardekhoCityPriceVariantStats(
                    apiVariants=0,
                    storedVariants=0,
                    matchedWithSourceTrims=0,
                    unmatchedSourceTrims=(len(job.source_trims)),
                    unmatchedApiVariants=0,
                )
            ),
            source=(
                CardekhoCityPriceSource(
                    carDocumentId=(job.source_car_document_id),
                    carRunId=(job.source_car_run_id),
                    cityDocumentId=(job.source_city_document_id),
                    cityRunId=(job.source_city_run_id),
                )
            ),
            request=(
                CardekhoCityPriceRequest(
                    modelSlug=(job.model_slug),
                    cityId=(job.city_id),
                    url=(job.request_url_value),
                )
            ),
        )

    async def execute(
        self,
        job: CardekhoCityPriceJob,
    ) -> CardekhoCityPrice:
        endpoint = CARDEKHO_MODEL_PRICE

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarDekho model-price API"
            )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "cityId": (job.city_id),
                "modelSlug": (job.model_slug),
                "url": (job.request_url_value),
            },
            headers={
                **endpoint.default_headers,
                "Referer": (f"{CARDEKHO_BASE_URL}/{job.request_url_value}"),
            },
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho model-price API "
                "returned an invalid response. "
                "Expected an object"
            )

        status = response_data.get("status")

        status_code = response_data.get("statusCode")

        if status is False or (
            isinstance(
                status_code,
                int,
            )
            and not isinstance(
                status_code,
                bool,
            )
            and status_code >= 400
        ):
            raise ExternalResponseError(
                "CarDekho model-price API "
                "returned an unsuccessful "
                "response: "
                f"status={status!r}, "
                "status_code="
                f"{status_code!r}"
            )

        data = response_data.get("data")

        if not isinstance(
            data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho model-price response does not contain a valid data object"
            )

        raw_price_sections = data.get("priceDetailSection")

        if (
            not isinstance(
                raw_price_sections,
                list,
            )
            or not raw_price_sections
        ):
            redirect_url = self._redirect_url(data)

            if redirect_url is not None:
                return self._unavailable_record(
                    job=job,
                )

        price_detail = self._find_price_detail(
            data,
            job=job,
        )

        returned_status = self._optional_string(price_detail.get("modelStatus"))

        if returned_status is not None and returned_status.upper() != "CURRENT":
            raise ExternalResponseError(
                "CarDekho returned a "
                "non-current price detail "
                "for a CURRENT job: "
                f"model_id={job.model_id}, "
                "returned_status="
                f"{returned_status!r}"
            )

        price_available = not self._as_bool(
            price_detail.get("priceNotAvailable"),
            default=False,
        )

        (
            variants,
            variant_stats,
        ) = self._variants(
            price_detail,
            job=job,
            price_available=(price_available),
        )

        if not variants:
            price_available = False

        price_url = self._optional_string(price_detail.get("priceUrl"))

        if price_url is None:
            price_url = f"/{job.request_url_value}"

        return CardekhoCityPrice(
            modelId=job.model_id,
            modelName=job.model_name,
            modelSlug=job.model_slug,
            modelStatus=job.model_status,
            brandId=job.brand_id,
            brandName=job.brand_name,
            brandSlug=job.brand_slug,
            carSlug=job.car_slug,
            cityId=job.city_id,
            cityName=job.city_name,
            cityDisplayName=(job.city_display_name),
            citySlug=job.city_slug,
            isPopularCity=(job.is_popular_city),
            priceAvailable=(price_available),
            priceRange=(
                self._price_range(
                    price_detail,
                    variants=variants,
                )
            ),
            priceDetailTitle=(
                self._optional_string(price_detail.get("priceDetailTitle"))
            ),
            modelUrl=(self._optional_string(price_detail.get("modelUrl"))),
            priceUrl=price_url,
            estimatedText=(self._optional_string(price_detail.get("estimatedText"))),
            fuelTypes=(
                self._fuel_types(
                    price_detail,
                    variants=variants,
                )
            ),
            transmissionTypes=(
                self._split_values(price_detail.get("transmissionType"))
            ),
            totalVariants=len(variants),
            variants=variants,
            variantStats=(variant_stats),
            source=(
                CardekhoCityPriceSource(
                    carDocumentId=(job.source_car_document_id),
                    carRunId=(job.source_car_run_id),
                    cityDocumentId=(job.source_city_document_id),
                    cityRunId=(job.source_city_run_id),
                )
            ),
            request=(
                CardekhoCityPriceRequest(
                    modelSlug=(job.model_slug),
                    cityId=(job.city_id),
                    url=(job.request_url_value),
                )
            ),
        )
