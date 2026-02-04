import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ReviewState:
    location_id: str
    review_id: str


class StateStore:
    def __init__(self, database_path: str) -> None:
        self._path = Path(database_path)
        self._connection = sqlite3.connect(self._path)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS responded_reviews (
                    location_id TEXT NOT NULL,
                    review_id TEXT NOT NULL,
                    PRIMARY KEY (location_id, review_id)
                )
                """
            )

    def has_responded(self, location_id: str, review_id: str) -> bool:
        cursor = self._connection.execute(
            "SELECT 1 FROM responded_reviews WHERE location_id = ? AND review_id = ?",
            (location_id, review_id),
        )
        return cursor.fetchone() is not None

    def mark_responded(self, entries: Iterable[ReviewState]) -> None:
        with self._connection:
            self._connection.executemany(
                "INSERT OR IGNORE INTO responded_reviews (location_id, review_id) VALUES (?, ?)",
                [(entry.location_id, entry.review_id) for entry in entries],
            )

    def close(self) -> None:
        self._connection.close()
