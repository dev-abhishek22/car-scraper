from __future__ import annotations

import html
import re
from collections.abc import Mapping
from html.parser import HTMLParser
from typing import Any
from urllib.parse import unquote, urlsplit

from src.clients.async_client import (
    AsyncExternalHttpClient,
)
from src.clients.client import (
    ExternalResponseError,
)
from src.external.constants.cardekho import (
    CARDEKHO_BASE_URL,
    CARDEKHO_MODEL_OVERVIEW,
)

SLUG_PATTERN = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
)

COMPARE_URL_PATTERN = re.compile(
    r"^/compare/(?P<comparison>.+)\.htm$",
    re.IGNORECASE,
)

SOURCE_MODEL_STATUSES = {
    "CURRENT",
    "UPCOMING",
    "DISCONTINUED",
}

API_MODEL_STATUS_MAP = {
    "CURRENT": "CURRENT",
    "UPCOMING": "UPCOMING",
    "EXPIRED": "DISCONTINUED",
    "DISCONTINUED": "DISCONTINUED",
}

REDIRECT_STATUS_CODES = {
    301,
    302,
    307,
    308,
}


class _AnchorHTMLParser(HTMLParser):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            convert_charrefs=True,
        )

        self.href: str | None = None
        self.title: str | None = None
        self._text_parts: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.lower() != "a":
            return

        attributes = dict(attrs)

        href = attributes.get("href")

        if isinstance(href, str) and href.strip():
            self.href = href.strip()

        title = attributes.get("title")

        if isinstance(title, str) and title.strip():
            self.title = title.strip()

    def handle_data(
        self,
        data: str,
    ) -> None:
        normalized_data = data.strip()

        if normalized_data:
            self._text_parts.append(normalized_data)

    @property
    def text(
        self,
    ) -> str | None:
        text = " ".join(self._text_parts).strip()

        return text or None


class CarDekhoCarsExecutor:
    """
    Fetch and normalize one CarDekho model-overview response.

    The endpoint has two request styles:

    - Normalized request:
      brandSlug=maruti, modelSlug=brezza, url=maruti/brezza

    - Legacy canonical request:
      brandSlug=Audi, modelSlug=Audi_A6,
      url=carmodels/Audi/Audi_A6

    Some normalized requests return an API-level redirect object instead
    of overView. The executor follows that redirect once and continues to
    store the original canonical identity from cardekho_models.
    """

    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self._client = client

    @staticmethod
    def _validate_positive_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return value

    @staticmethod
    def _coerce_positive_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int:
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            return value

        if isinstance(value, str):
            normalized_value = value.strip()

            if normalized_value.isdigit():
                integer_value = int(normalized_value)

                if integer_value > 0:
                    return integer_value

        raise ValueError(f"{field_name} must be a positive integer")

    @staticmethod
    def _normalize_optional_positive_integer(
        value: Any,
    ) -> int | None:
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            return value

        if isinstance(value, str):
            normalized_value = value.strip()

            if normalized_value.isdigit():
                integer_value = int(normalized_value)

                if integer_value > 0:
                    return integer_value

        return None

    @staticmethod
    def _validate_non_empty_string(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _normalize_optional_string(
        value: Any,
    ) -> str | None:
        if not isinstance(value, str):
            return None

        normalized_value = html.unescape(
            value,
        ).strip()

        return normalized_value or None

    @classmethod
    def _normalize_slug(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str:
        normalized_value = (
            cls._validate_non_empty_string(
                value,
                field_name=field_name,
            )
            .lower()
            .replace("_", "-")
            .replace(" ", "-")
        )

        normalized_value = re.sub(
            r"-+",
            "-",
            normalized_value,
        ).strip("-")

        if not SLUG_PATTERN.fullmatch(
            normalized_value,
        ):
            raise ValueError(
                f"{field_name} contains invalid characters: {normalized_value!r}"
            )

        return normalized_value

    @classmethod
    def _normalize_optional_slug(
        cls,
        value: Any,
    ) -> str | None:
        if not isinstance(value, str):
            return None

        normalized_value = value.strip().lower().replace("_", "-").replace(" ", "-")

        normalized_value = re.sub(
            r"-+",
            "-",
            normalized_value,
        ).strip("-")

        if not normalized_value:
            return None

        if not SLUG_PATTERN.fullmatch(
            normalized_value,
        ):
            return None

        return normalized_value

    @staticmethod
    def _normalize_optional_url(
        value: Any,
    ) -> str | None:
        if not isinstance(value, str):
            return None

        normalized_value = html.unescape(
            value,
        ).strip()

        if not normalized_value:
            return None

        return normalized_value

    @staticmethod
    def _normalize_optional_float(
        value: Any,
    ) -> float | None:
        if isinstance(value, bool) or not isinstance(
            value,
            (
                int,
                float,
            ),
        ):
            return None

        return float(value)

    @staticmethod
    def _normalize_optional_non_negative_integer(
        value: Any,
    ) -> int | None:
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            return value

        if isinstance(value, str):
            normalized_value = value.strip()

            if normalized_value.isdigit():
                return int(normalized_value)

        return None

    @staticmethod
    def _normalize_model_status(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        normalized_status = value.strip().upper()

        if normalized_status not in SOURCE_MODEL_STATUSES:
            raise ValueError(f"{field_name} must be CURRENT, UPCOMING, or DISCONTINUED")

        return normalized_status

    @staticmethod
    def _normalize_api_model_status(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise ExternalResponseError(f"{field_name} must be a string")

        normalized_status = value.strip().upper()

        mapped_status = API_MODEL_STATUS_MAP.get(
            normalized_status,
        )

        if mapped_status is None:
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                f"an unsupported status: {normalized_status!r}"
            )

        return mapped_status

    @classmethod
    def _validate_model(
        cls,
        model: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(model, Mapping):
            raise ValueError("model must be an object")

        model_status = cls._normalize_model_status(
            model.get("modelStatus"),
            field_name="model.modelStatus",
        )

        is_upcoming = model.get("isUpcoming")

        if not isinstance(is_upcoming, bool):
            raise ValueError("model.isUpcoming must be a boolean")

        expected_is_upcoming = model_status == "UPCOMING"

        if is_upcoming != expected_is_upcoming:
            raise ValueError(
                "model.isUpcoming does not match "
                f"model.modelStatus: status={model_status!r}, "
                f"is_upcoming={is_upcoming!r}"
            )

        return {
            "id": cls._validate_positive_integer(
                model.get("id"),
                field_name="model.id",
            ),
            "brandName": cls._validate_non_empty_string(
                model.get("brandName"),
                field_name="model.brandName",
            ),
            "brandSlug": cls._normalize_slug(
                model.get("brandSlug"),
                field_name="model.brandSlug",
            ),
            "name": cls._validate_non_empty_string(
                model.get("name"),
                field_name="model.name",
            ),
            "slug": cls._normalize_slug(
                model.get("slug"),
                field_name="model.slug",
            ),
            "modelName": cls._validate_non_empty_string(
                model.get("modelName"),
                field_name="model.modelName",
            ),
            "modelStatus": model_status,
            "isUpcoming": is_upcoming,
            "expectedLaunchDate": (
                cls._normalize_optional_string(
                    model.get("expectedLaunchDate"),
                )
            ),
        }

    @staticmethod
    def _parse_anchor_html(
        value: Any,
    ) -> dict[str, str | None]:
        if not isinstance(value, str):
            return {
                "text": None,
                "title": None,
                "href": None,
            }

        normalized_value = value.strip()

        if not normalized_value:
            return {
                "text": None,
                "title": None,
                "href": None,
            }

        parser = _AnchorHTMLParser()

        try:
            parser.feed(normalized_value)
            parser.close()
        except Exception:
            return {
                "text": None,
                "title": None,
                "href": None,
            }

        return {
            "text": parser.text,
            "title": parser.title,
            "href": parser.href,
        }

    @classmethod
    def _extract_other_car_slug(
        cls,
        *,
        comparison_url: str | None,
        current_car_slug: str,
    ) -> str | None:
        if comparison_url is None:
            return None

        match = COMPARE_URL_PATTERN.fullmatch(
            comparison_url,
        )

        if match is None:
            return None

        comparison = match.group(
            "comparison",
        )

        car_slugs = comparison.split(
            "-and-",
        )

        if len(car_slugs) != 2:
            return None

        normalized_car_slugs: list[str] = []

        for car_slug in car_slugs:
            normalized_car_slug = cls._normalize_optional_slug(
                car_slug,
            )

            if normalized_car_slug is not None:
                normalized_car_slugs.append(
                    normalized_car_slug,
                )

        if len(normalized_car_slugs) != 2:
            return None

        for car_slug in normalized_car_slugs:
            if car_slug != current_car_slug:
                return car_slug

        return None

    @classmethod
    def _split_car_slug(
        cls,
        *,
        car_slug: str,
        model_name: str | None,
        short_name: str | None,
        preferred_brand_slug: str | None = None,
    ) -> tuple[
        str | None,
        str | None,
    ]:
        normalized_car_slug = cls._normalize_optional_slug(
            car_slug,
        )

        if normalized_car_slug is None:
            return (
                None,
                None,
            )

        if preferred_brand_slug is not None:
            normalized_preferred_brand_slug = cls._normalize_optional_slug(
                preferred_brand_slug,
            )

            if normalized_preferred_brand_slug is not None:
                prefix = f"{normalized_preferred_brand_slug}-"

                if normalized_car_slug.startswith(
                    prefix,
                ):
                    model_slug = normalized_car_slug[len(prefix) :]

                    if model_slug:
                        return (
                            normalized_preferred_brand_slug,
                            model_slug,
                        )

        possible_model_names = [
            short_name,
            model_name,
        ]

        for possible_model_name in possible_model_names:
            model_slug = cls._normalize_optional_slug(
                possible_model_name,
            )

            if model_slug is None:
                continue

            suffix = f"-{model_slug}"

            if normalized_car_slug.endswith(
                suffix,
            ):
                brand_slug = normalized_car_slug[: -len(suffix)]

                if brand_slug:
                    return (
                        brand_slug,
                        model_slug,
                    )

        return (
            None,
            None,
        )

    @staticmethod
    def _validate_response_envelope(
        response_data: Any,
    ) -> Mapping[str, Any]:
        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                "an invalid response. Expected an object"
            )

        response_status = response_data.get(
            "status",
        )

        if response_status is False:
            raise ExternalResponseError(
                "CarDekho model-overview API returned status=false"
            )

        response_status_code = response_data.get(
            "statusCode",
        )

        if (
            isinstance(response_status_code, int)
            and not isinstance(
                response_status_code,
                bool,
            )
            and response_status_code != 200
        ):
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                f"statusCode={response_status_code}"
            )

        data = response_data.get(
            "data",
        )

        if not isinstance(
            data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho model-overview API response "
                "does not contain a valid data object"
            )

        return data

    @classmethod
    def _parse_redirect_request(
        cls,
        *,
        data: Mapping[str, Any],
    ) -> dict[str, str] | None:
        redirect = data.get("redirect")

        if not isinstance(redirect, Mapping):
            return None

        redirect_status_code = redirect.get("statusCode")

        if (
            redirect_status_code is not None
            and redirect_status_code not in REDIRECT_STATUS_CODES
        ):
            return None

        redirect_url = redirect.get("redirectURL")

        if not isinstance(redirect_url, str):
            return None

        normalized_redirect_url = html.unescape(redirect_url).strip()

        if not normalized_redirect_url:
            return None

        split_result = urlsplit(normalized_redirect_url)

        if split_result.scheme or split_result.netloc:
            return None

        redirect_path = unquote(split_result.path)

        if not redirect_path.startswith("/"):
            redirect_path = f"/{redirect_path}"

        path_parts = [part for part in redirect_path.split("/") if part]

        if len(path_parts) == 3 and path_parts[0].lower() == "carmodels":
            request_brand_slug = path_parts[1]
            request_model_slug = path_parts[2]

        elif len(path_parts) == 2:
            request_brand_slug = path_parts[0]
            request_model_slug = path_parts[1]

        else:
            return None

        if not request_brand_slug.strip() or not request_model_slug.strip():
            return None

        request_url = redirect_path.lstrip("/")

        if split_result.query:
            request_url = f"{request_url}?{split_result.query}"

        return {
            "brandSlug": request_brand_slug,
            "modelSlug": request_model_slug,
            "url": request_url,
            "refererPath": redirect_path,
        }

    async def _fetch_response(
        self,
        *,
        request_brand_slug: str,
        request_model_slug: str,
        request_url: str,
        referer_path: str,
    ) -> Mapping[str, Any]:
        endpoint = CARDEKHO_MODEL_OVERVIEW

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for "
                "the CarDekho model-overview API"
            )

        normalized_referer_path = referer_path

        if not normalized_referer_path.startswith("/"):
            normalized_referer_path = f"/{normalized_referer_path}"

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "brandSlug": request_brand_slug,
                "modelSlug": request_model_slug,
                "url": request_url,
            },
            headers={
                **endpoint.default_headers,
                "Referer": (f"{CARDEKHO_BASE_URL}" f"{normalized_referer_path}"),
            },
        )

        if not isinstance(response_data, Mapping):
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                "an invalid response. Expected an object"
            )

        return response_data

    async def _fetch_data_with_redirect(
        self,
        *,
        source_brand_slug: str,
        source_model_slug: str,
    ) -> Mapping[str, Any]:
        initial_request_url = f"{source_brand_slug}/{source_model_slug}"

        initial_referer_path = f"/{source_brand_slug}/{source_model_slug}"

        response_data = await self._fetch_response(
            request_brand_slug=source_brand_slug,
            request_model_slug=source_model_slug,
            request_url=initial_request_url,
            referer_path=initial_referer_path,
        )

        data = self._validate_response_envelope(response_data)

        raw_overview = data.get("overView")

        if isinstance(raw_overview, Mapping):
            return data

        redirect_request = self._parse_redirect_request(
            data=data,
        )

        if redirect_request is None:
            data_keys = sorted(str(key) for key in data.keys())

            raise ExternalResponseError(
                "CarDekho model-overview API response "
                "does not contain a valid overView object: "
                f"model={source_brand_slug}:"
                f"{source_model_slug}, "
                f"data_keys={data_keys}, "
                "redirect_url=None"
            )

        redirected_request_signature = (
            redirect_request["brandSlug"],
            redirect_request["modelSlug"],
            redirect_request["url"],
        )

        initial_request_signature = (
            source_brand_slug,
            source_model_slug,
            initial_request_url,
        )

        if redirected_request_signature == initial_request_signature:
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                "a redirect to the same request: "
                f"model={source_brand_slug}:"
                f"{source_model_slug}, "
                "redirect_url="
                f"{redirect_request['refererPath']!r}"
            )

        redirected_response_data = await self._fetch_response(
            request_brand_slug=redirect_request["brandSlug"],
            request_model_slug=redirect_request["modelSlug"],
            request_url=redirect_request["url"],
            referer_path=redirect_request["refererPath"],
        )

        redirected_data = self._validate_response_envelope(
            redirected_response_data,
        )

        redirected_overview = redirected_data.get("overView")

        if not isinstance(
            redirected_overview,
            Mapping,
        ):
            second_redirect = self._parse_redirect_request(
                data=redirected_data,
            )

            data_keys = sorted(str(key) for key in redirected_data.keys())

            second_redirect_url = (
                second_redirect["refererPath"] if second_redirect is not None else None
            )

            raise ExternalResponseError(
                "CarDekho model-overview API response "
                "does not contain a valid overView object "
                "after following one redirect: "
                f"model={source_brand_slug}:"
                f"{source_model_slug}, "
                f"data_keys={data_keys}, "
                "redirect_url="
                f"{second_redirect_url!r}"
            )

        return redirected_data

    @classmethod
    def _validate_response_identity(
        cls,
        *,
        data: Mapping[str, Any],
        overview: Mapping[str, Any],
        expected_model_id: int,
        expected_brand_slug: str,
        expected_model_slug: str,
        expected_model_status: str,
    ) -> None:
        response_model_ids: list[int] = []

        data_model_id = data.get("modelId")

        if data_model_id is not None:
            try:
                response_model_ids.append(
                    cls._coerce_positive_integer(
                        data_model_id,
                        field_name="data.modelId",
                    )
                )
            except ValueError as error:
                raise ExternalResponseError(str(error)) from error

        overview_model_id = overview.get("id")

        if overview_model_id is not None:
            try:
                response_model_ids.append(
                    cls._coerce_positive_integer(
                        overview_model_id,
                        field_name="data.overView.id",
                    )
                )
            except ValueError as error:
                raise ExternalResponseError(str(error)) from error

        if not response_model_ids:
            raise ExternalResponseError(
                "CarDekho model-overview API response "
                "does not contain a usable model ID"
            )

        if any(
            response_model_id != expected_model_id
            for response_model_id in response_model_ids
        ):
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                "a different model ID: "
                f"expected={expected_model_id}, "
                f"found={response_model_ids}"
            )

        response_brand_slug = cls._normalize_optional_slug(
            overview.get("brandSlug"),
        )

        if (
            response_brand_slug is not None
            and response_brand_slug != expected_brand_slug
        ):
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                "a different brand slug: "
                f"expected={expected_brand_slug!r}, "
                f"found={response_brand_slug!r}"
            )

        response_model_slug = cls._normalize_optional_slug(
            overview.get("modelSlug"),
        )

        if (
            response_model_slug is not None
            and response_model_slug != expected_model_slug
        ):
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                "a different model slug: "
                f"expected={expected_model_slug!r}, "
                f"found={response_model_slug!r}"
            )

        response_model_status = cls._normalize_api_model_status(
            overview.get("modelStatus"),
            field_name="data.overView.modelStatus",
        )

        if response_model_status != expected_model_status:
            raise ExternalResponseError(
                "CarDekho model-overview API returned "
                "a different model status: "
                f"expected={expected_model_status!r}, "
                f"found={response_model_status!r}"
            )

    @classmethod
    def _parse_overview(
        cls,
        overview: Mapping[str, Any],
    ) -> dict[str, Any]:
        display_name = cls._normalize_optional_string(
            overview.get("name"),
        ) or cls._normalize_optional_string(
            overview.get("modelName"),
        )

        short_name = cls._normalize_optional_string(
            overview.get("modelShortName"),
        )

        return {
            "displayName": display_name,
            "shortName": short_name,
            "modelUrl": cls._normalize_optional_url(
                overview.get("modelUrl"),
            ),
            "reviewUrl": cls._normalize_optional_url(
                overview.get("reviewUrl"),
            ),
            "image": cls._normalize_optional_url(
                overview.get("image"),
            ),
            "webpImage": cls._normalize_optional_url(
                overview.get("webp"),
            ),
            "brandLogo": cls._normalize_optional_url(
                overview.get("brandLogo"),
            ),
            "rating": cls._normalize_optional_float(
                overview.get("rating"),
            ),
            "reviewCount": (
                cls._normalize_optional_non_negative_integer(
                    overview.get("reviewCount"),
                )
            ),
        }

    @classmethod
    def _collect_raw_variants(
        cls,
        variant_table: Any,
    ) -> list[Mapping[str, Any]]:
        if not isinstance(
            variant_table,
            Mapping,
        ):
            return []

        raw_variants: list[Mapping[str, Any]] = []

        variant_list = variant_table.get(
            "variantList",
        )

        if isinstance(variant_list, list):
            for variant in variant_list:
                if isinstance(variant, Mapping):
                    raw_variants.append(
                        variant,
                    )

        child_groups = variant_table.get(
            "childs",
        )

        if isinstance(child_groups, list):
            for child_group in child_groups:
                if not isinstance(
                    child_group,
                    Mapping,
                ):
                    continue

                items = child_group.get(
                    "items",
                )

                if not isinstance(items, list):
                    continue

                for variant in items:
                    if isinstance(variant, Mapping):
                        raw_variants.append(
                            variant,
                        )

        return raw_variants

    @classmethod
    def _parse_variants(
        cls,
        *,
        variant_table: Any,
        parent_model_status: str,
    ) -> list[dict[str, Any]]:
        raw_variants = cls._collect_raw_variants(
            variant_table,
        )

        variants: list[dict[str, Any]] = []

        seen_ids: set[int] = set()
        seen_slugs: set[str] = set()

        for raw_variant in raw_variants:
            variant_id = cls._normalize_optional_positive_integer(
                raw_variant.get("centralId"),
            )

            # Keep Cardekho's variantSlug as returned.
            # Do not apply the strict model-slug regex because Cardekho
            # legitimately uses values such as kia-seltos-hte-(o).
            variant_slug = cls._normalize_optional_string(
                raw_variant.get("variantSlug"),
            )

            if variant_id is None and variant_slug is None:
                continue

            if variant_id is not None and variant_id in seen_ids:
                continue

            if variant_slug is not None and variant_slug in seen_slugs:
                continue

            variant_name = (
                cls._normalize_optional_string(
                    raw_variant.get("name"),
                )
                or cls._normalize_optional_string(
                    raw_variant.get("text"),
                )
                or cls._normalize_optional_string(
                    raw_variant.get("title"),
                )
            )

            short_name = cls._normalize_optional_string(
                raw_variant.get(
                    "variantShortName",
                ),
            )

            variant_url = cls._normalize_optional_url(
                raw_variant.get("url"),
            )

            raw_variant_status = raw_variant.get(
                "variantStatus",
            )

            if raw_variant_status is None:
                variant_status = parent_model_status
            else:
                try:
                    variant_status = cls._normalize_api_model_status(
                        raw_variant_status,
                        field_name="variant.variantStatus",
                    )
                except ExternalResponseError:
                    variant_status = parent_model_status

            if variant_id is not None:
                seen_ids.add(
                    variant_id,
                )

            if variant_slug is not None:
                seen_slugs.add(
                    variant_slug,
                )

            variants.append(
                {
                    "id": variant_id,
                    "name": variant_name,
                    "shortName": short_name,
                    "slug": variant_slug,
                    "url": variant_url,
                    "status": variant_status,
                }
            )

        return variants

    @classmethod
    def _parse_similar_cars(
        cls,
        *,
        compare_with: Any,
        current_brand_slug: str,
        current_model_slug: str,
    ) -> list[dict[str, Any]]:
        if not isinstance(
            compare_with,
            Mapping,
        ):
            return []

        raw_similar_cars = compare_with.get(
            "list",
        )

        if not isinstance(
            raw_similar_cars,
            list,
        ):
            return []

        current_car_slug = f"{current_brand_slug}-{current_model_slug}"

        similar_cars: list[dict[str, Any]] = []

        seen_car_slugs: set[str] = set()

        for raw_similar_car in raw_similar_cars:
            if not isinstance(
                raw_similar_car,
                Mapping,
            ):
                continue

            brand_slug = cls._normalize_optional_slug(
                raw_similar_car.get(
                    "brandSlug",
                ),
            )

            model_slug = cls._normalize_optional_slug(
                raw_similar_car.get(
                    "modelSlug",
                ),
            )

            if brand_slug is None or model_slug is None:
                continue

            car_slug = f"{brand_slug}-{model_slug}"

            if car_slug == current_car_slug:
                continue

            if car_slug in seen_car_slugs:
                continue

            seen_car_slugs.add(
                car_slug,
            )

            similar_cars.append(
                {
                    "brandName": (
                        cls._normalize_optional_string(
                            raw_similar_car.get(
                                "brandName",
                            ),
                        )
                    ),
                    "brandSlug": brand_slug,
                    "modelName": (
                        cls._normalize_optional_string(
                            raw_similar_car.get(
                                "modelName",
                            ),
                        )
                    ),
                    "shortName": (
                        cls._normalize_optional_string(
                            raw_similar_car.get(
                                "name",
                            ),
                        )
                    ),
                    "modelSlug": model_slug,
                    "carSlug": car_slug,
                    "modelUrl": (
                        cls._normalize_optional_url(
                            raw_similar_car.get(
                                "modelUrl",
                            ),
                        )
                    ),
                    "comparisonUrl": (
                        cls._normalize_optional_url(
                            raw_similar_car.get(
                                "compareUrl",
                            ),
                        )
                    ),
                    "compareText": (
                        cls._normalize_optional_string(
                            raw_similar_car.get(
                                "ctaText",
                            ),
                        )
                    ),
                    "image": (
                        cls._normalize_optional_url(
                            raw_similar_car.get(
                                "image",
                            ),
                        )
                    ),
                    "webpImage": (
                        cls._normalize_optional_url(
                            raw_similar_car.get(
                                "webpImage",
                            ),
                        )
                    ),
                }
            )

        return similar_cars

    @classmethod
    def _parse_comparisons(
        cls,
        *,
        nav_compare: Any,
        current_brand_slug: str,
        current_model_slug: str,
    ) -> list[dict[str, Any]]:
        if not isinstance(nav_compare, list):
            return []

        current_car_slug = f"{current_brand_slug}-{current_model_slug}"

        comparisons: list[dict[str, Any]] = []

        seen_car_slugs: set[str] = set()

        for raw_comparison in nav_compare:
            if not isinstance(
                raw_comparison,
                Mapping,
            ):
                continue

            comparison_url = cls._normalize_optional_url(
                raw_comparison.get(
                    "compareURL",
                ),
            )

            target_model_name = cls._normalize_optional_string(
                raw_comparison.get(
                    "modelName2",
                ),
            )

            target_short_name = cls._normalize_optional_string(
                raw_comparison.get(
                    "shortModelName2",
                ),
            )

            target_car_slug = cls._extract_other_car_slug(
                comparison_url=comparison_url,
                current_car_slug=current_car_slug,
            )

            if target_car_slug is None:
                continue

            (
                target_brand_slug,
                target_model_slug,
            ) = cls._split_car_slug(
                car_slug=target_car_slug,
                model_name=target_model_name,
                short_name=target_short_name,
            )

            if target_brand_slug is None or target_model_slug is None:
                continue

            if target_car_slug in seen_car_slugs:
                continue

            seen_car_slugs.add(
                target_car_slug,
            )

            comparisons.append(
                {
                    "brandName": (
                        cls._normalize_optional_string(
                            raw_comparison.get(
                                "modelBrandName2",
                            ),
                        )
                    ),
                    "brandSlug": target_brand_slug,
                    "modelName": target_model_name,
                    "shortName": target_short_name,
                    "modelSlug": target_model_slug,
                    "carSlug": target_car_slug,
                    "comparisonUrl": comparison_url,
                    "compareText": (
                        cls._normalize_optional_string(
                            raw_comparison.get(
                                "displayText",
                            ),
                        )
                        or cls._normalize_optional_string(
                            raw_comparison.get(
                                "title",
                            ),
                        )
                    ),
                    "image": (
                        cls._normalize_optional_url(
                            raw_comparison.get(
                                "image2",
                            ),
                        )
                    ),
                    "webpImage": (
                        cls._normalize_optional_url(
                            raw_comparison.get(
                                "webpImage2",
                            ),
                        )
                    ),
                }
            )

        return comparisons

    @classmethod
    def _parse_old_generation_comparison(
        cls,
        *,
        overview: Mapping[str, Any],
        current_brand_slug: str,
        current_model_slug: str,
    ) -> dict[str, Any] | None:
        raw_old_generation = overview.get(
            "oldGenerationComparison",
        )

        if not isinstance(
            raw_old_generation,
            Mapping,
        ):
            raw_old_generation = {}

        parsed_anchor = cls._parse_anchor_html(
            overview.get(
                "expireModelCompareText",
            ),
        )

        model_name = cls._normalize_optional_string(
            raw_old_generation.get(
                "modelName",
            ),
        )

        comparison_url = cls._normalize_optional_url(
            raw_old_generation.get(
                "comparisonUrl",
            ),
        ) or cls._normalize_optional_url(
            parsed_anchor.get("href"),
        )

        compare_text = cls._normalize_optional_string(
            parsed_anchor.get("text"),
        ) or cls._normalize_optional_string(
            parsed_anchor.get("title"),
        )

        badge_text = cls._normalize_optional_string(
            raw_old_generation.get(
                "badgeText",
            ),
        )

        image = cls._normalize_optional_url(
            raw_old_generation.get(
                "imageUrl",
            ),
        )

        if model_name is None and compare_text is not None:
            prefix = "Compare with Old Generation "

            if compare_text.startswith(prefix):
                model_name = compare_text[len(prefix) :].strip() or None

        if (
            model_name is None
            and comparison_url is None
            and compare_text is None
            and badge_text is None
            and image is None
        ):
            return None

        current_car_slug = f"{current_brand_slug}-{current_model_slug}"

        old_car_slug = cls._extract_other_car_slug(
            comparison_url=comparison_url,
            current_car_slug=current_car_slug,
        )

        old_brand_slug: str | None = None
        old_model_slug: str | None = None

        if old_car_slug is not None:
            (
                old_brand_slug,
                old_model_slug,
            ) = cls._split_car_slug(
                car_slug=old_car_slug,
                model_name=model_name,
                short_name=model_name,
                preferred_brand_slug=current_brand_slug,
            )

        if old_car_slug is None and model_name is not None:
            normalized_model_name_slug = cls._normalize_optional_slug(
                model_name,
            )

            if normalized_model_name_slug is not None:
                brand_prefix = f"{current_brand_slug}-"

                if normalized_model_name_slug.startswith(
                    brand_prefix,
                ):
                    old_model_slug = normalized_model_name_slug[len(brand_prefix) :]
                else:
                    old_model_slug = normalized_model_name_slug

                old_brand_slug = current_brand_slug
                old_car_slug = f"{old_brand_slug}-{old_model_slug}"

        return {
            "modelName": model_name,
            "brandSlug": old_brand_slug,
            "modelSlug": old_model_slug,
            "carSlug": old_car_slug,
            "compareText": compare_text,
            "badgeText": badge_text,
            "comparisonUrl": comparison_url,
            "image": image,
        }

    async def execute(
        self,
        *,
        model: Mapping[str, Any],
    ) -> dict[str, Any]:
        validated_model = self._validate_model(
            model,
        )

        model_id = validated_model["id"]
        brand_slug = validated_model["brandSlug"]
        model_slug = validated_model["slug"]
        model_status = validated_model["modelStatus"]

        data = await self._fetch_data_with_redirect(
            source_brand_slug=brand_slug,
            source_model_slug=model_slug,
        )

        raw_overview = data.get(
            "overView",
        )

        if not isinstance(
            raw_overview,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho model-overview API response "
                "does not contain a valid overView object"
            )

        self._validate_response_identity(
            data=data,
            overview=raw_overview,
            expected_model_id=model_id,
            expected_brand_slug=brand_slug,
            expected_model_slug=model_slug,
            expected_model_status=model_status,
        )

        overview = self._parse_overview(
            raw_overview,
        )

        variants = self._parse_variants(
            variant_table=data.get(
                "variantTable",
            ),
            parent_model_status=model_status,
        )

        comparisons = self._parse_comparisons(
            nav_compare=data.get(
                "navComapre",
            ),
            current_brand_slug=brand_slug,
            current_model_slug=model_slug,
        )

        similar_cars = self._parse_similar_cars(
            compare_with=data.get(
                "compareWith",
            ),
            current_brand_slug=brand_slug,
            current_model_slug=model_slug,
        )

        old_generation_comparison = self._parse_old_generation_comparison(
            overview=raw_overview,
            current_brand_slug=brand_slug,
            current_model_slug=model_slug,
        )

        return {
            "overview": overview,
            "totalVariants": len(variants),
            "variants": variants,
            "totalComparisons": len(comparisons),
            "compareWith": comparisons,
            "totalSimilarCars": len(similar_cars),
            "similarCars": similar_cars,
            "oldGenerationComparison": old_generation_comparison,
        }
