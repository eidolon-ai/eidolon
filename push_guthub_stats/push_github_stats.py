import argparse
import json
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

    try:
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
            print(f"Failed to retrieve traffic data. Clones status code: {clones_response.status_code}, Views status code: {views_response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None


def insert_into_posthog(event_name: str, counts: List[Tuple[str, int]], posthog_api_key, posthog_project_key):
    # Set the PostHog API endpoint URL
    posthog_url = "https://app.posthog.com/capture/"

    # Set the headers with the PostHog API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {posthog_api_key}"
    }

    # Iterate over each day's traffic data
    for timestamp, count in counts:

        # Check if data for the current day already exists in PostHog
        if not is_data_duplicated(event_name, timestamp, posthog_api_key, posthog_project_key):
            # Prepare the data payload
            data = {
                "event": event_name,
                "api_key": posthog_project_key,
                "distinct_id": "github_traffic",
                "properties": {
                    "count": count,
                    "timestamp": timestamp
                },
                "timestamp": timestamp,
            }

            try:
                # Send a POST request to the PostHog API endpoint
                response = requests.post(posthog_url, headers=headers, json=data)

                # Check if the request was successful
                if response.status_code == 200:
                    print(f"Data inserted successfully for event {event_name}, timestamp: {timestamp}")
                else:
                    print(f"Failed to insert data for timestamp: {timestamp}. Status code: {response.status_code} {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while inserting data for timestamp: {timestamp}. Error: {e}")
        else:
            print(f"Data already exists for event {event_name}, timestamp: {timestamp}. Skipping insertion.")


def is_data_duplicated(event_name, timestamp, posthog_api_key, posthog_project_key):
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
            }
        ])
    }

    try:
        # Send a GET request to the PostHog API endpoint to check for existing data
        response = requests.get(posthog_url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the events from the response
            events = response.json()["results"]

            print("Got events ", len(events))
            # Check if any events exist for the given timestamp
            if len(events) > 0:
                return True
            else:
                return False
        else:
            print(f"Failed to retrieve events from PostHog. Status code: {response.status_code}, {response.text}")
            return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking for duplicates. Error: {e}")
        return True


def main():
    owner = "eidolon-ai"
    repo = "eidolon"

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Extract GitHub traffic data and insert into PostHog")
    parser.add_argument("--access-token", required=True, help="GitHub access token")
    parser.add_argument("--api-key", required=True, help="PostHog API key")
    parser.add_argument("--project-key", required=True, help="PostHog Project key")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract the GitHub clones and views per day
    clones, views = extract_github_traffic(owner, repo, args.access_token)
    if clones:
        clones_per_day = [(clone["timestamp"], clone["count"]) for clone in clones]
        unique_clones_per_day = [(clone["timestamp"], clone["uniques"]) for clone in clones]
        insert_into_posthog("github_clones", clones_per_day, args.api_key, args.project_key)
        insert_into_posthog("github_unique_clones", unique_clones_per_day, args.api_key, args.project_key)
    if views:
        views_per_day = [(view["timestamp"], view["count"]) for view in views]
        unique_views_per_day = [(view["timestamp"], view["uniques"]) for view in views]
        insert_into_posthog("github_views", views_per_day, args.api_key, args.project_key)
        insert_into_posthog("github_unique_views", unique_views_per_day, args.api_key, args.project_key)


if __name__ == "__main__":
    main()
