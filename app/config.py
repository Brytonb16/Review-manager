import os
from dataclasses import dataclass
from typing import Dict

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    google_account_id: str
    location_ids: list[str]
    response_templates: Dict[str, str]
    database_path: str
    reviews_page_size: int
    max_reviews_per_location: int
    default_language: str


DEFAULT_TEMPLATES = {
    "5": "Thanks so much for the 5-star review, {name}! We're excited to serve you again.",
    "4": "Thanks for the great review, {name}! Let us know if there's anything we can do to earn that 5th star.",
    "3": "Thanks for the feedback, {name}. We're always working to improve and would love to learn more.",
    "2": "Thanks for sharing, {name}. We're sorry to hear we missed the mark and would like to make it right.",
    "1": "Thanks for letting us know, {name}. We want to make this right—please contact us so we can help.",
    "fallback": "Thanks for your feedback, {name}! We appreciate you."
}


def _parse_templates(raw_templates: str | None) -> Dict[str, str]:
    if not raw_templates:
        return DEFAULT_TEMPLATES

    templates: Dict[str, str] = {}
    for entry in raw_templates.split("|"):
        if "=" not in entry:
            continue
        key, value = entry.split("=", 1)
        templates[key.strip()] = value.strip()

    merged = {**DEFAULT_TEMPLATES, **templates}
    return merged


def load_settings() -> Settings:
    load_dotenv()

    account_id = os.environ.get("GOOGLE_ACCOUNT_ID", "").strip()
    if not account_id:
        raise ValueError("GOOGLE_ACCOUNT_ID is required")

    raw_locations = os.environ.get("LOCATION_IDS", "")
    location_ids = [loc.strip() for loc in raw_locations.split(",") if loc.strip()]
    if not location_ids:
        raise ValueError("LOCATION_IDS is required and must contain at least one location")

    response_templates = _parse_templates(os.environ.get("RESPONSE_TEMPLATES"))

    database_path = os.environ.get("DATABASE_PATH", "review_state.sqlite3")
    reviews_page_size = int(os.environ.get("REVIEWS_PAGE_SIZE", "50"))
    max_reviews_per_location = int(os.environ.get("MAX_REVIEWS_PER_LOCATION", "200"))
    default_language = os.environ.get("DEFAULT_LANGUAGE", "en")

    return Settings(
        google_account_id=account_id,
        location_ids=location_ids,
        response_templates=response_templates,
        database_path=database_path,
        reviews_page_size=reviews_page_size,
        max_reviews_per_location=max_reviews_per_location,
        default_language=default_language,
    )
