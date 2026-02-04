# Review Auto Responder

This project provides a small Python service that automatically responds to Google Business Profile reviews for multiple store locations. Configure your account ID, location IDs, and response templates, then run the script on a schedule (cron, GitHub Actions, etc.).

## Features
- Responds to new reviews for multiple locations.
- Template-based responses by star rating.
- Local SQLite state to avoid duplicate replies.
- Dry-run mode for safe previews.
- Optional web experience inspired by BirdEye for teams that prefer a dashboard.

## Prerequisites
1. A Google Business Profile account with access to all locations.
2. Enable the Business Profile API and Reviews API for your Google Cloud project.
3. Application Default Credentials set up for the service account or user.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the environment template and fill it out:
```bash
cp .env.example .env
```

## Configuration
| Variable | Description |
| --- | --- |
| `GOOGLE_ACCOUNT_ID` | The numeric Google Business Profile account ID. |
| `LOCATION_IDS` | Comma-separated location IDs for your stores. |
| `RESPONSE_TEMPLATES` | Optional overrides for reply templates (format: `5=Great!|4=Thanks!`). |
| `DATABASE_PATH` | SQLite file for tracking replied reviews. |
| `REVIEWS_PAGE_SIZE` | Page size for the API requests. |
| `MAX_REVIEWS_PER_LOCATION` | Max reviews to scan per location each run. |
| `DEFAULT_LANGUAGE` | Language code for responses. |

## Run
Dry run:
```bash
python -m app.main --dry-run
```

Send replies:
```bash
python -m app.main
```

## Web dashboard
If you want a BirdEye-style experience, start the web interface:
```bash
python -m app.web
```

Then open `http://localhost:8000` in your browser.

## Recommended workflow
1. Run in dry-run first to confirm templates.
2. Schedule regular runs (cron/systemd/GitHub Actions).
3. Monitor the SQLite DB to confirm replies are recorded.

## Notes
- Replies are only sent for reviews without existing replies.
- Customize `RESPONSE_TEMPLATES` for your brand voice.
