import argparse
import json
import os
from datetime import datetime
from typing import List, Dict

import dotenv
import requests


def extract_github_traffic(repo_owner, repo_name, access_token, action, version):
    # Set the API endpoint URLs
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/{action}"

    # Set the headers with the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": f"application/{version}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    page = 0
    response = ['placeholder']
    while response:
        page += 1
        params = {
            "per_page": 100,  # max
            "page": page
        }

        # Send GET requests to the API endpoints
        response = requests.get(url, headers=headers, params=params)

        # Check if the requests were successful
        response.raise_for_status()
        response = response.json()
        for record in response:
            yield record


def insert_into_posthog(event_name: str, repo: str, data: List[Dict[str, any]], posthog_api_key, posthog_project_key, skip_older, dry_run):
    # Iterate over each day's traffic data
    for event in data:
        if "timestamp" not in event:
            raise ValueError("Timestamp is required in the event data")
        timestamp = event["timestamp"]
        date = timestamp.split("T")[0]
        # check if the date is more than 10 days old
        if skip_older > 0 and ((datetime.now() - datetime.strptime(date, "%Y-%m-%d")).days > skip_older):
            # print(f"Skipping data for date {date} as it is more than 10 days old.")
            continue

        print(f"Processing {repo}/{event_name} for date {timestamp}, data: {event}")
        posthog_update_if_needed(event_name, repo, timestamp, event, posthog_api_key, posthog_project_key, dry_run)


def posthog_update_if_needed(event_name, repo: str, timestamp, event, posthog_api_key, posthog_project_key, dry_run):
    # Set the PostHog API endpoint URL
    posthog_url = "https://app.posthog.com/capture/"
    # Set the headers with the PostHog API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {posthog_api_key}"
    }
    # Check if data for the current day already exists in PostHog
    events = get_existing_events(event_name, repo, timestamp, posthog_api_key, posthog_project_key)
    should_insert = not events or len(events) == 0
    if should_insert:
        # Prepare the data payload
        data = {
            "event": event_name,
            "api_key": posthog_project_key,
            "distinct_id": event.get("distinct_id") or "github_traffic",
            "properties": {
                **event,
                "timestamp": timestamp,
                "repo": repo,
                "insertion_timestamp": datetime.now().isoformat(),
            },
            "timestamp": timestamp,
        }

        if dry_run:
            print(f"Would have sent data: {data}")
        else:
            # Send a POST request to the PostHog API endpoint
            print("Sending data to PostHog", data)
            response = requests.post(posthog_url, headers=headers, json=data)
            response.raise_for_status()
    else:
        print(f"Data for date {timestamp} already exists in PostHog", len(events), events[0]["properties"]["timestamp"])


def get_existing_events(event_name, repo, timestamp, posthog_api_key, posthog_project_key):
    # Set the PostHog API endpoint URL for querying events
    posthog_url = "https://app.posthog.com/api/event/"

    # Set the headers with the PostHog API key
    headers = {
        "Authorization": f"Bearer {posthog_api_key}"
    }

    # Set the query parameters
    params = {
        "event": event_name,
        "api_key": posthog_project_key,
        "properties": json.dumps([
            {
                "key": "timestamp",
                "value": timestamp,
                "operator": "exact"
            }, {
                "key": "repo",
                "value": repo,
                "operator": "exact"
            }
        ])
    }

    response = requests.get(posthog_url, headers=headers, params=params)
    response.raise_for_status()
    events = response.json()["results"]
    return events


def run_script(version, action, event_name, extract_data):
    dotenv.load_dotenv()

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Extract GitHub traffic data and insert into PostHog")
    parser.add_argument("--access-token", required=False, help="GitHub access token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--api-key", required=False, help="PostHog API key", default=os.environ.get("POSTHOG_API_KEY"))
    parser.add_argument("--project-key", required=False, help="PostHog Project key", default=os.environ.get("POSTHOG_PROJECT_KEY"))
    parser.add_argument("--repo", required=True, help="The repo to gather stats from in the form of owner/repo")
    parser.add_argument("--dry-run", required=False, help="Just print what would have happened", default=False, action="store_true")
    parser.add_argument("--skip-older", required=False, help="Skip events older than <days> in the past", default=21, type=int)

    # Parse the command-line arguments
    args = parser.parse_args()

    if not args.access_token:
        raise ValueError("GitHub access token is required")
    if not args.api_key:
        raise ValueError("PostHog API key is required")
    if not args.project_key:
        raise ValueError("PostHog project key is required")

    owner, repo = args.repo.split("/")
    if not owner or not repo:
        raise ValueError("Invalid repo format. Please provide the repo in the format owner/repo")

    # Extract the GitHub clones and views per day
    transformed_data = []
    for event in extract_github_traffic(owner, repo, args.access_token, action, version):
        extracted_data = extract_data(event)
        extracted_data["repo"] = repo
        transformed_data.append(extracted_data)
    transformed_data.sort(key=lambda x: x["timestamp"])

    if transformed_data:
        insert_into_posthog(event_name, repo, transformed_data, args.api_key, args.project_key, args.skip_older, args.dry_run)
