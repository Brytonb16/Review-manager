from __future__ import annotations

import argparse
from typing import Iterable

from app.client import build_reviews_client
from app.config import load_settings
from app.reviews import build_reply, filter_needing_reply, list_reviews, respond_to_review
from app.state import ReviewState, StateStore


def process_location(
    reviews_client,
    settings,
    store: StateStore,
    location_id: str,
    dry_run: bool,
) -> list[ReviewState]:
    reviews = list(
        list_reviews(
            reviews_client,
            settings.google_account_id,
            location_id,
            settings.reviews_page_size,
            settings.max_reviews_per_location,
        )
    )
    to_reply = filter_needing_reply(reviews)

    responded: list[ReviewState] = []
    for review in to_reply:
        if store.has_responded(location_id, review.review_id):
            continue
        reply_text = build_reply(settings.response_templates, review)
        if not dry_run:
            respond_to_review(
                reviews_client,
                settings.google_account_id,
                review,
                reply_text,
                settings.default_language,
            )
        responded.append(ReviewState(location_id=location_id, review_id=review.review_id))

    return responded


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Auto-respond to Google Business Profile reviews for multiple locations."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print intended replies without sending them.",
    )
    return parser.parse_args()


def print_dry_run(reviews: Iterable[ReviewState]) -> None:
    if not reviews:
        print("No new reviews to respond to.")
        return
    print("Reviews queued for response:")
    for entry in reviews:
        print(f"- location={entry.location_id} review={entry.review_id}")


def main() -> None:
    args = parse_args()
    settings = load_settings()
    reviews_client = build_reviews_client()
    store = StateStore(settings.database_path)

    pending: list[ReviewState] = []
    try:
        for location_id in settings.location_ids:
            responses = process_location(
                reviews_client,
                settings,
                store,
                location_id,
                args.dry_run,
            )
            pending.extend(responses)

        if args.dry_run:
            print_dry_run(pending)
        else:
            store.mark_responded(pending)
            print(f"Sent {len(pending)} replies.")
    finally:
        store.close()


if __name__ == "__main__":
    main()
