from datetime import datetime

from scripts.base_push_github_stats import run_script


def extract_data(event):
    return {
        "owner_id": event["id"],
        "owner_login": event["login"],
        "distinct_id": event["login"],
        "email": event.get("email") or "",
        "timestamp": event.get("starred_at") or datetime.now().isoformat(),
    }


def main():
    raise "Broken -- need a date time field to"
    run_script("vnd.github+json", "subscribers", "gh_watchers", extract_data)


if __name__ == "__main__":
    main()
