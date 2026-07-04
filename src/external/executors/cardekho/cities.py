from __future__ import annotations

import ast
import importlib
import json
import re
from collections.abc import Mapping
from typing import Any

from src.clients.async_client import (
    AsyncExternalHttpClient,
)
from src.clients.client import (
    ExternalResponseError,
)
from src.external.constants.cardekho import (
    CARDEKHO_CITIES_BUNDLE,
    CARDEKHO_CITIES_BUNDLE_URL,
)

JSON_PARSE_PATTERN = re.compile(
    r"JSON\s*\.\s*parse\s*\(",
    re.IGNORECASE,
)

DIRECT_CITY_ARRAY_PATTERNS = (
    re.compile(
        r'\[\s*\{\s*"CID"\s*:',
    ),
    re.compile(
        r"\[\s*\{\s*'CID'\s*:",
    ),
)


CARDEKHO_CITIES_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Referer": "https://www.cardekho.com/",
}


class CarDekhoCitiesExecutor:
    """
    Fetch and normalize the CarDekho cities webpack bundle.

    The source bundle currently contains the complete city
    array inside a JSON.parse(...) expression. The parser is
    intentionally defensive and supports:

    1. A direct JSON array response.
    2. A city JSON array embedded directly in JavaScript.
    3. A JSON array encoded inside JSON.parse('...').
    4. A JSON array encoded inside JSON.parse("...").

    Duplicate source rows are merged by CID.
    """

    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self._client = client

    @staticmethod
    def _validate_non_empty_string(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise ExternalResponseError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise ExternalResponseError(f"{field_name} cannot be empty")

        return normalized_value

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

        raise ExternalResponseError(f"{field_name} must be a positive integer")

    @staticmethod
    def _coerce_boolean(
        value: Any,
    ) -> bool:
        if isinstance(value, bool):
            return value

        if isinstance(value, int) and not isinstance(value, bool):
            return value == 1

        if isinstance(value, str):
            return value.strip().lower() in {
                "1",
                "true",
                "yes",
            }

        return False

    @staticmethod
    def _is_city_array(
        value: Any,
    ) -> bool:
        if not isinstance(value, list) or not value:
            return False

        checked_rows = 0

        for item in value[:10]:
            if not isinstance(
                item,
                Mapping,
            ):
                return False

            if "CID" not in item or "CN" not in item:
                return False

            checked_rows += 1

        return checked_rows > 0

    @classmethod
    def _decode_direct_response(
        cls,
        bundle_text: str,
    ) -> list[Any] | None:
        stripped_text = bundle_text.lstrip()

        if not stripped_text.startswith("["):
            return None

        try:
            parsed_value = json.loads(stripped_text)

        except json.JSONDecodeError:
            return None

        if cls._is_city_array(parsed_value):
            return parsed_value

        return None

    @classmethod
    def _decode_embedded_city_array(
        cls,
        bundle_text: str,
    ) -> list[Any] | None:
        decoder = json.JSONDecoder()

        for pattern in DIRECT_CITY_ARRAY_PATTERNS:
            for match in pattern.finditer(bundle_text):
                start_index = match.start()

                try:
                    (
                        parsed_value,
                        _,
                    ) = decoder.raw_decode(bundle_text[start_index:])

                except json.JSONDecodeError:
                    continue

                if cls._is_city_array(parsed_value):
                    return parsed_value

        return None

    @staticmethod
    def _extract_javascript_string_literal(
        bundle_text: str,
        *,
        start_index: int,
    ) -> tuple[str, int]:
        index = start_index
        bundle_length = len(bundle_text)

        while index < bundle_length and bundle_text[index].isspace():
            index += 1

        if index >= bundle_length:
            raise ExternalResponseError(
                "CarDekho cities bundle ended before the JSON.parse argument"
            )

        quote = bundle_text[index]

        if quote not in {
            "'",
            '"',
            "`",
        }:
            raise ExternalResponseError(
                "CarDekho cities JSON.parse argument is not a JavaScript string literal"
            )

        literal_start = index
        index += 1

        escaped = False

        while index < bundle_length:
            character = bundle_text[index]

            if escaped:
                escaped = False

            elif character == "\\":
                escaped = True

            elif character == quote:
                return (
                    bundle_text[literal_start : index + 1],
                    index + 1,
                )

            index += 1

        raise ExternalResponseError(
            "CarDekho cities bundle contains an unterminated JSON.parse string literal"
        )

    @staticmethod
    def _decode_javascript_string_literal(
        string_literal: str,
    ) -> str:
        quote = string_literal[0]

        if quote == "`":
            body = string_literal[1:-1]

            if "${" in body:
                raise ExternalResponseError(
                    "CarDekho cities template literal "
                    "contains unsupported interpolation"
                )

            string_literal = repr(body)

        try:
            decoded_value = ast.literal_eval(string_literal)

        except (
            SyntaxError,
            ValueError,
        ) as error:
            raise ExternalResponseError(
                "CarDekho cities JavaScript string literal could not be decoded"
            ) from error

        if not isinstance(
            decoded_value,
            str,
        ):
            raise ExternalResponseError(
                "CarDekho cities JSON.parse argument did not decode to a string"
            )

        return decoded_value

    @classmethod
    def _decode_json_parse_city_array(
        cls,
        bundle_text: str,
    ) -> list[Any] | None:
        parse_errors: list[ExternalResponseError] = []

        for match in JSON_PARSE_PATTERN.finditer(bundle_text):
            try:
                (
                    string_literal,
                    literal_end,
                ) = cls._extract_javascript_string_literal(
                    bundle_text,
                    start_index=match.end(),
                )

                closing_index = literal_end

                while (
                    closing_index < len(bundle_text)
                    and bundle_text[closing_index].isspace()
                ):
                    closing_index += 1

                if (
                    closing_index >= len(bundle_text)
                    or bundle_text[closing_index] != ")"
                ):
                    raise ExternalResponseError(
                        "CarDekho cities bundle contains an invalid JSON.parse call"
                    )

                decoded_json = cls._decode_javascript_string_literal(string_literal)

                parsed_value = json.loads(decoded_json)

            except (
                ExternalResponseError,
                json.JSONDecodeError,
            ) as error:
                if isinstance(
                    error,
                    ExternalResponseError,
                ):
                    parse_errors.append(error)

                else:
                    parse_errors.append(
                        ExternalResponseError(
                            "CarDekho cities JSON.parse payload contains invalid JSON"
                        )
                    )

                continue

            if cls._is_city_array(parsed_value):
                return parsed_value

        if parse_errors:
            raise ExternalResponseError(
                "CarDekho cities bundle contained "
                "JSON.parse calls, but no valid city "
                "array could be decoded"
            ) from parse_errors[-1]

        return None

    @staticmethod
    def _looks_like_cities_bundle(
        value: str,
    ) -> bool:
        return "JSON.parse" in value and '"CID"' in value and '"CN"' in value

    @classmethod
    def _decode_bundle_response(
        cls,
        *,
        response_content: bytes,
        content_encoding: str | None,
    ) -> str:
        if not isinstance(
            response_content,
            bytes,
        ):
            raise ExternalResponseError(
                "CarDekho cities response content must be bytes"
            )

        if not response_content:
            raise ExternalResponseError("CarDekho cities response body is empty")

        try:
            plain_text = response_content.decode("utf-8")

        except UnicodeDecodeError:
            plain_text = None

        if plain_text is not None and cls._looks_like_cities_bundle(plain_text):
            return plain_text

        try:
            brotli_module = importlib.import_module("brotli")

        except ImportError as error:
            first_bytes = response_content[:32].hex()

            raise ExternalResponseError(
                "CarDekho cities response is Brotli "
                "compressed, but the Python 'brotli' "
                "package is not installed. Run: "
                "uv add brotli. "
                f"content_encoding={content_encoding!r}, "
                f"content_length={len(response_content)}, "
                f"first_bytes={first_bytes}"
            ) from error

        try:
            decompressed_content = brotli_module.decompress(response_content)

        except Exception as error:
            first_bytes = response_content[:32].hex()

            raise ExternalResponseError(
                "CarDekho cities response could not "
                "be decoded as plain UTF-8 or Brotli: "
                f"content_encoding={content_encoding!r}, "
                f"content_length={len(response_content)}, "
                f"first_bytes={first_bytes}"
            ) from error

        try:
            bundle_text = decompressed_content.decode("utf-8")

        except UnicodeDecodeError as error:
            raise ExternalResponseError(
                "Decompressed CarDekho cities bundle is not valid UTF-8"
            ) from error

        if not cls._looks_like_cities_bundle(bundle_text):
            preview = " ".join(bundle_text[:240].split())

            raise ExternalResponseError(
                "Decompressed CarDekho response does "
                "not look like the cities bundle: "
                "content_length="
                f"{len(bundle_text)}, "
                f"content_preview={preview!r}"
            )

        return bundle_text

    @classmethod
    def _extract_raw_cities(
        cls,
        bundle_text: str,
        *,
        content_type: str | None = None,
        response_url: str | None = None,
    ) -> list[Any]:
        normalized_bundle_text = cls._validate_non_empty_string(
            bundle_text,
            field_name="cities bundle",
        )

        direct_response = cls._decode_direct_response(normalized_bundle_text)

        if direct_response is not None:
            return direct_response

        embedded_array = cls._decode_embedded_city_array(normalized_bundle_text)

        if embedded_array is not None:
            return embedded_array

        json_parse_array = cls._decode_json_parse_city_array(normalized_bundle_text)

        if json_parse_array is not None:
            return json_parse_array

        preview = " ".join(normalized_bundle_text[:240].split())

        raise ExternalResponseError(
            "CarDekho cities bundle does not contain "
            "a recognizable city array: "
            f"response_url={response_url!r}, "
            f"content_type={content_type!r}, "
            "content_length="
            f"{len(normalized_bundle_text)}, "
            f"content_preview={preview!r}"
        )

    @classmethod
    def _normalize_regions(
        cls,
        value: Any,
        *,
        row_index: int,
    ) -> list[dict[str, Any]]:
        if value is None:
            return []

        if not isinstance(value, list):
            raise ExternalResponseError(
                f"CarDekho city REG must be an array: row_index={row_index}"
            )

        regions: list[dict[str, Any]] = []

        seen_region_ids: set[int] = set()

        for (
            region_index,
            raw_region,
        ) in enumerate(value):
            if not isinstance(
                raw_region,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarDekho city region must be an "
                    "object: "
                    f"row_index={row_index}, "
                    f"region_index={region_index}"
                )

            region_id = cls._coerce_positive_integer(
                raw_region.get("RID"),
                field_name=(f"cities[{row_index}].REG[{region_index}].RID"),
            )

            region_name = cls._validate_non_empty_string(
                raw_region.get("RN"),
                field_name=(f"cities[{row_index}].REG[{region_index}].RN"),
            )

            if region_id in seen_region_ids:
                continue

            seen_region_ids.add(region_id)

            regions.append(
                {
                    "regionId": region_id,
                    "regionName": region_name,
                }
            )

        return regions

    @classmethod
    def _normalize_raw_city(
        cls,
        raw_city: Any,
        *,
        row_index: int,
    ) -> dict[str, Any]:
        if not isinstance(
            raw_city,
            Mapping,
        ):
            raise ExternalResponseError(
                f"CarDekho city row must be an object: row_index={row_index}"
            )

        city_id = cls._coerce_positive_integer(
            raw_city.get("CID"),
            field_name=(f"cities[{row_index}].CID"),
        )

        city_name = cls._validate_non_empty_string(
            raw_city.get("CN"),
            field_name=(f"cities[{row_index}].CN"),
        )

        raw_display_name = raw_city.get("CDN")

        if raw_display_name is None:
            display_name = city_name

        else:
            display_name = cls._validate_non_empty_string(
                raw_display_name,
                field_name=(f"cities[{row_index}].CDN"),
            )

        return {
            "cityId": city_id,
            "cityName": city_name,
            "displayName": display_name,
            "isPopular": (cls._coerce_boolean(raw_city.get("P"))),
            "isPrime": (cls._coerce_boolean(raw_city.get("isPrime"))),
            "regions": (
                cls._normalize_regions(
                    raw_city.get("REG"),
                    row_index=row_index,
                )
            ),
        }

    @staticmethod
    def _append_unique_string(
        values: list[str],
        value: str,
    ) -> None:
        normalized_value = value.casefold()

        if any(
            existing_value.casefold() == normalized_value for existing_value in values
        ):
            return

        values.append(value)

    @classmethod
    def _merge_cities(
        cls,
        raw_cities: list[Any],
    ) -> list[dict[str, Any]]:
        cities_by_id: dict[
            int,
            dict[str, Any],
        ] = {}

        for (
            row_index,
            raw_city,
        ) in enumerate(raw_cities):
            city = cls._normalize_raw_city(
                raw_city,
                row_index=row_index,
            )

            city_id = city["cityId"]

            existing_city = cities_by_id.get(city_id)

            if existing_city is None:
                aliases: list[str] = []

                cls._append_unique_string(
                    aliases,
                    city["cityName"],
                )

                cls._append_unique_string(
                    aliases,
                    city["displayName"],
                )

                cities_by_id[city_id] = {
                    "cityId": city_id,
                    "cityName": (city["cityName"]),
                    "displayName": (city["displayName"]),
                    "aliases": aliases,
                    "isPopular": (city["isPopular"]),
                    "isPrime": (city["isPrime"]),
                    "regions": list(city["regions"]),
                }

                continue

            cls._append_unique_string(
                existing_city["aliases"],
                city["cityName"],
            )

            cls._append_unique_string(
                existing_city["aliases"],
                city["displayName"],
            )

            if (
                existing_city["displayName"].casefold()
                != existing_city["cityName"].casefold()
                and city["displayName"].casefold()
                == existing_city["cityName"].casefold()
            ):
                existing_city["displayName"] = city["displayName"]

            existing_city["isPopular"] = bool(
                existing_city["isPopular"] or city["isPopular"]
            )

            existing_city["isPrime"] = bool(existing_city["isPrime"] or city["isPrime"])

            existing_region_ids = {
                region["regionId"] for region in existing_city["regions"]
            }

            for region in city["regions"]:
                if region["regionId"] in existing_region_ids:
                    continue

                existing_region_ids.add(region["regionId"])

                existing_city["regions"].append(region)

        cities = list(cities_by_id.values())

        for city in cities:
            city["regions"].sort(key=lambda region: region["regionId"])

        cities.sort(key=lambda city: city["cityId"])

        return cities

    async def execute(
        self,
    ) -> dict[str, Any]:
        endpoint = CARDEKHO_CITIES_BUNDLE

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarDekho cities bundle"
            )

        response = await self._client.get(
            endpoint=endpoint.path,
            params=endpoint.default_params,
            headers={
                **endpoint.default_headers,
                **CARDEKHO_CITIES_REQUEST_HEADERS,
            },
        )

        response_headers = getattr(
            response,
            "headers",
            {},
        )

        content_encoding: str | None = None

        if isinstance(
            response_headers,
            Mapping,
        ):
            raw_content_encoding = response_headers.get("content-encoding")

            if isinstance(
                raw_content_encoding,
                str,
            ):
                content_encoding = raw_content_encoding

        bundle_text = self._decode_bundle_response(
            response_content=(response.content),
            content_encoding=(content_encoding),
        )

        response_url = str(
            getattr(
                response,
                "url",
                CARDEKHO_CITIES_BUNDLE_URL,
            )
        )

        content_type: str | None = None

        if isinstance(
            response_headers,
            Mapping,
        ):
            raw_content_type = response_headers.get("content-type")

            if isinstance(
                raw_content_type,
                str,
            ):
                content_type = raw_content_type

        raw_cities = self._extract_raw_cities(
            bundle_text,
            content_type=content_type,
            response_url=response_url,
        )

        cities = self._merge_cities(raw_cities)

        if not cities:
            raise ExternalResponseError(
                "CarDekho cities bundle returned no usable cities"
            )

        return {
            "sourceUrl": response_url,
            "rawCityCount": len(raw_cities),
            "uniqueCityCount": len(cities),
            "duplicateCityRows": (len(raw_cities) - len(cities)),
            "cities": cities,
        }
