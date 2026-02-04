from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Iterator

from app.templates import choose_template, render_template


@dataclass(frozen=True)
class Review:
    review_id: str
    location_id: str
    star_rating: int
    reviewer_name: str | None
    has_reply: bool


def list_reviews(
    reviews_client: Any,
    account_id: str,
    location_id: str,
    page_size: int,
    max_results: int,
) -> Iterator[Review]:
    location_name = f"accounts/{account_id}/locations/{location_id}"
    request = reviews_client.accounts().locations().reviews().list(
        parent=location_name,
        pageSize=page_size,
        orderBy="update_time desc",
    )

    fetched = 0
    while request is not None and fetched < max_results:
        response = request.execute()
        for raw in response.get("reviews", []):
            if fetched >= max_results:
                break
            fetched += 1
            yield Review(
                review_id=raw.get("reviewId", ""),
                location_id=location_id,
                star_rating=int(raw.get("starRating", 0)),
                reviewer_name=(raw.get("reviewer", {}) or {}).get("displayName"),
                has_reply=bool(raw.get("reviewReply")),
            )

        request = reviews_client.accounts().locations().reviews().list_next(
            previous_request=request,
            previous_response=response,
        )


def build_reply(templates: dict[str, str], review: Review) -> str:
    template = choose_template(templates, review.star_rating)
    return render_template(template, review.reviewer_name)


def respond_to_review(
    reviews_client: Any,
    account_id: str,
    review: Review,
    reply_text: str,
    language_code: str,
) -> None:
    review_name = (
        f"accounts/{account_id}/locations/{review.location_id}/reviews/{review.review_id}"
    )
    reviews_client.accounts().locations().reviews().updateReply(
        name=review_name,
        body={
            "comment": reply_text,
            "languageCode": language_code,
        },
    ).execute()


def filter_needing_reply(reviews: Iterable[Review]) -> list[Review]:
    return [review for review in reviews if review.review_id and not review.has_reply]
