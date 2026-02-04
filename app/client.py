from __future__ import annotations

from typing import Any

from google.auth import default
from googleapiclient.discovery import build


def build_business_profile_client() -> Any:
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/business.manage"])
    return build("mybusinessbusinessinformation", "v1", credentials=credentials)


def build_reviews_client() -> Any:
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/business.manage"])
    return build("mybusiness", "v4", credentials=credentials)
