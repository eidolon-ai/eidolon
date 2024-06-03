from datetime import datetime

from scripts.base_push_github_stats import run_script


def extract_data(event):
    return {
        "owner_id": event["user"]["id"],
        "owner_login": event["user"]["login"],
        "distinct_id": event["user"]["login"],
        "email": event.get("email") or "",
        "timestamp": event["starred_at"]
    }


def main():
    run_script("vnd.github.v3.star+json", "stargazers", "gh_stars", extract_data)


if __name__ == "__main__":
    main()
