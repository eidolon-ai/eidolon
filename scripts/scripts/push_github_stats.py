import argparse
import json
from datetime import datetime
from typing import List, Tuple

import requests


def extract_github_traffic(repo_owner, repo_name, access_token):
    # Set the API endpoint URLs
    clones_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/traffic/clones"
    views_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/traffic/views"

    # Set the headers with the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json"
    }

    # Send GET requests to the API endpoints
    clones_response = requests.get(clones_url, headers=headers)
    views_response = requests.get(views_url, headers=headers)

    # Check if the requests were successful
    if clones_response.status_code == 200 and views_response.status_code == 200:
        # Extract the traffic data from the responses
        clones_per_day = clones_response.json()["clones"]
        views_per_day = views_response.json()["views"]

        return clones_per_day, views_per_day
    else:
        raise RuntimeError(f"Failed to retrieve traffic data. Clones status code: {clones_response.status_code}, Views status code: {views_response.status_code}")


def insert_into_posthog_with_count(distinct_id: str, event_name: str, counts: List[Tuple[str, int]], posthog_api_key, posthog_project_key, skip_older: int, dry_run: bool, repo: str):
    # Iterate over each day's traffic data
    for timestamp, count in counts:
        print(f"Processing data for date {timestamp}, count: {count}")
        date = timestamp.split("T")[0]
        # check if the date is more than 10 days old
        if skip_older > 0 and ((datetime.now() - datetime.strptime(date, "%Y-%m-%d")).days > 10):
            # print(f"Skipping data for date {date} as it is more than 10 days old.")
            continue

        posthog_update_if_needed(distinct_id, event_name, timestamp, count, posthog_api_key, posthog_project_key, dry_run, repo)


def posthog_update_if_needed(distinct_id: str, event_name, timestamp, count, posthog_api_key, posthog_project_key, dry_run, repo="eidolon"):
    # Set the PostHog API endpoint URL
    posthog_url = "https://app.posthog.com/capture/"
    # Set the headers with the PostHog API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {posthog_api_key}"
    }
    # Check if data for the current day already exists in PostHog
    events = get_existing_events(event_name, timestamp, posthog_api_key, posthog_project_key, repo)
    should_insert = True
    existing_count = 0
    if events:
        for event in events:
            existing_count += event["properties"]["count"]

        if existing_count != count:
            print(f"Updating existing data for {repo}/{event_name} date {timestamp} existing_count: {existing_count}, need: {count}, with new count {count - existing_count}")
            count = count - existing_count
        else:
            should_insert = False
    if should_insert:
        # Prepare the data payload
        data = {
            "event": event_name,
            "api_key": posthog_project_key,
            "distinct_id": distinct_id,
            "properties": {
                "count": count,
                "timestamp": timestamp,
                "repo": repo,
            },
            "timestamp": timestamp,
        }

        if dry_run:
            print(f"Would have sent data: {data}")
        else:
            # Send a POST request to the PostHog API endpoint
            response = requests.post(posthog_url, headers=headers, json=data)
            response.raise_for_status()
    else:
        print(f"Data for date {timestamp} already exists in PostHog", existing_count, count)


def get_existing_events(event_name, timestamp, posthog_api_key, posthog_project_key, repo):
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

    # # Extract the GitHub clones and views per day
    # # clones, views = extract_github_traffic(owner, repo, args.access_token)
    # timestamps = ["2024-02-12", "2024-02-13", "2024-02-14", "2024-02-15", "2024-02-16", "2024-02-17", "2024-02-18", "2024-02-19", "2024-02-20", "2024-02-21", "2024-02-22",
    #               "2024-02-23", "2024-02-24", "2024-02-25", "2024-02-26", "2024-02-27", "2024-02-28", "2024-02-29", "2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04",
    #               "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09", "2024-03-10", "2024-03-11", "2024-03-12", "2024-03-13", "2024-03-14", "2024-03-15",
    #               "2024-03-16", "2024-03-17", "2024-03-18", "2024-03-19", "2024-03-20", "2024-03-21", "2024-03-22", "2024-03-23", "2024-03-24", "2024-03-25", "2024-03-26",
    #               "2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30", "2024-03-31", "2024-04-01", "2024-04-02", "2024-04-03", "2024-04-04", "2024-04-05", "2024-04-06",
    #               "2024-04-07", "2024-04-08", "2024-04-09", "2024-04-10", "2024-04-11", "2024-04-12", "2024-04-13", "2024-04-14", "2024-04-15", "2024-04-16", "2024-04-17",
    #               "2024-04-18", "2024-04-19", "2024-04-20", "2024-04-21", "2024-04-22"]
    # unique_clones = [1, 13, 2, 5, 7, 4, 2, 5, 6, 11, 11, 1, 4, 2, 9, 5, 4, 7, 5, 1, 0, 7, 7, 4, 8, 9, 4, 4, 6, 1, 2, 2, 3, 1, 1, 6, 15, 5, 9, 12, 10, 1, 7, 2, 2, 1, 2, 2, 1, 2, 11,
    #                  4, 3, 7, 7, 2, 2, 10, 15, 17, 18, 9, 9, 13, 31, 26, 37, 36, 19, 3, 12]
    # cloners = [6, 132, 2, 50, 40, 10, 8, 26, 28, 69, 158, 7, 10, 2, 110, 34, 41, 25, 27, 1, 0, 66, 28, 20, 20, 44, 11, 38, 14, 2, 3, 3, 8, 1, 4, 69, 201, 32, 112, 57, 53, 1, 17,
    #            18,
    #            3, 1, 3, 2, 1, 44, 93, 43, 19, 43, 32, 17, 7, 109, 115, 182, 94, 88, 49, 94, 186, 219, 291, 261, 91, 11, 59]
    # unique_views = [6, 132, 2, 50, 40, 10, 8, 26, 28, 69, 158, 7, 10, 2, 110, 34, 41, 25, 27, 1, 0, 66, 28, 20, 20, 44, 11, 38, 14, 2, 3, 3, 8, 1, 4, 69, 201, 32, 112, 57, 53, 1,
    #                 17, 18, 3, 1, 3, 2, 1, 44, 93, 43, 19, 43, 32, 17, 7, 109, 115, 182, 94, 88, 49, 94, 186, 219, 291, 261, 91, 11, 59]
    # viewers = [0, 11, 28, 41, 30, 33, 2, 43, 25, 50, 51,
    #            20, 1, 43, 139, 47, 22, 134, 16, 1, 4, 7,
    #            140, 60, 175, 58, 90, 57, 16, 162, 162,
    #            262, 224, 6, 6, 137, 468, 80, 71, 39, 43,
    #            19, 288, 12, 118, 32, 31, 14, 2, 48, 46,
    #            149, 43, 71, 82, 6, 9, 346, 340, 352,
    #            196, 86, 42, 232, 254, 303, 284, 258, 84,
    #            234, 40]


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Extract GitHub traffic data and insert into PostHog")
    parser.add_argument("--access-token", required=True, help="GitHub access token")
    parser.add_argument("--api-key", required=True, help="PostHog API key")
    parser.add_argument("--project-key", required=True, help="PostHog Project key")
    parser.add_argument("--dry-run", required=False, help="Just print what would have happened", default=False, action="store_true")
    parser.add_argument("--skip-older", required=False, help="Skip events older than <days> in the past", default=10, type=int)
    parser.add_argument("--repo", required=True, help="The repo to gather stats from in the form of owner/repo")

    # Parse the command-line arguments
    args = parser.parse_args()

    owner, repo = args.repo.split("/")
    if not owner or not repo:
        raise ValueError("Invalid repo format. Please provide the repo in the format owner/repo")

    # Extract the GitHub clones and views per day
    clones, views = extract_github_traffic(owner, repo, args.access_token)
    common_args = [args.api_key, args.project_key, args.skip_older, args.dry_run, repo]
    if clones:
        clones_per_day = [(clone["timestamp"], clone["count"]) for clone in clones]
        unique_clones_per_day = [(clone["timestamp"], clone["uniques"]) for clone in clones]
        insert_into_posthog_with_count("github_traffic", "gh_clones", clones_per_day, *common_args)
        insert_into_posthog_with_count("github_traffic", "gh_unique_clones", unique_clones_per_day, *common_args)
    if views:
        views_per_day = [(view["timestamp"], view["count"]) for view in views]
        unique_views_per_day = [(view["timestamp"], view["uniques"]) for view in views]
        insert_into_posthog_with_count("github_traffic", "gh_views", views_per_day, *common_args)
        insert_into_posthog_with_count("github_traffic", "gh_unique_views", unique_views_per_day, *common_args)


if __name__ == "__main__":
    main()
