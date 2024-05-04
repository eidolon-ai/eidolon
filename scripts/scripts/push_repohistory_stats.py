import argparse
import json
import os
from datetime import datetime

from scripts.push_github_stats import posthog_update_if_needed


def parse_repohistory_data(api_key, project_key):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repohistory_data.json')) as f:
        data = json.load(f)
        data = [arr[3] for arr in json.loads(data[1][3:])]
    dates = data[0]['data']['labels']

    event_names = {
        "Clones": "gh_clones",
        "Unique Cloners": "gh_unique_clones",
        "Views": "gh_views",
        "Unique Visitors": "gh_unique_views",
    }
    values = {event_names[dd['label']]: dd['data'] for d in data for dd in d['data']['datasets']}
    for label, count in values.items():
        print(f"Checking {label}...")
        for i in range(len(dates)-1):  # skip the last date as it's likely not complete
            pre_converted_timestamp = dates[i]
            # the next line converts the timestamp (currently in 2024-02-12) to the format that PostHog uses (YYYY-MM-DDTHH:MM:SSZ)
            timestamp = datetime.strptime(pre_converted_timestamp, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00Z")
            posthog_update_if_needed(
                label,
                timestamp,
                count[i],
                "phx_riZKSSe6BDTyXgeiduVvOaP4SGkADWauuMtVtiu5Agz",
                "phc_9lcmDyxVkji98ggIqy2XvyVcItnrgdrMQhZBFp6Du5d",
            )


def main():
    parser = argparse.ArgumentParser(description="""Extract Repohstory traffic data and insert into PostHog. 
    Repohistory does not provide an api, so data is populated from repohistory_data.json.""")
    parser.add_argument("--api-key", required=True, help="PostHog API key")
    parser.add_argument("--project-key", required=True, help="PostHog Project key")
    args = parser.parse_args()
    parse_repohistory_data(args.api_key, args.project_key)


if __name__ == "__main__":
    main()
