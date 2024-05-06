import argparse
import os
from datetime import datetime, timedelta
from typing import Tuple, List

import dotenv
import requests

from scripts.push_github_stats import insert_into_posthog_with_count


def get_first_day_of_period(period):
    today = datetime.now().date()
    if period == "last_day":
        return today - timedelta(days=1)
    elif period == "last_week":
        return today - timedelta(days=today.weekday() + 7)
    elif period == "last_month":
        first_day_of_current_month = today.replace(day=1)
        return first_day_of_current_month - timedelta(days=1)
    else:
        return None


def get_package_downloads(package_name):
    url = f"https://pypistats.org/api/packages/{package_name}/overall?mirrors=false"
    response = requests.get(url)
    data = response.json()

    downloads = data["data"]
    download_events: List[Tuple[str, int]] = []

    for day in downloads:
        download_events.append((day["date"] + "T00:00:00Z", int(day["downloads"])))
    return download_events


def run_script(event_name):
    dotenv.load_dotenv()

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Extract GitHub traffic data and insert into PostHog")
    parser.add_argument("--api-key", required=False, help="PostHog API key", default=os.environ.get("POSTHOG_API_KEY"))
    parser.add_argument("--project-key", required=False, help="PostHog Project key", default=os.environ.get("POSTHOG_PROJECT_KEY"))
    parser.add_argument("--package", required=True, help="The package to gather stats from")
    parser.add_argument("--dry-run", required=False, help="Just print what would have happened", default=False, action="store_true")
    parser.add_argument("--skip-older", required=False, help="Skip events older than <days> in the past", default=10, type=int)

    # Parse the command-line arguments
    args = parser.parse_args()

    if not args.api_key:
        raise ValueError("PostHog API key is required")
    if not args.project_key:
        raise ValueError("PostHog project key is required")

    # Extract the GitHub clones and views per day
    data = get_package_downloads(args.package)
    if data:
        insert_into_posthog_with_count("pypi_downloads", event_name, data, args.api_key, args.project_key, args.skip_older, args.dry_run)


def main():
    run_script("pypi_downloads")


if __name__ == "__main__":
    main()
