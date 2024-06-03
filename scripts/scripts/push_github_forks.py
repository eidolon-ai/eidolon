from scripts.base_push_github_stats import run_script


def extract_data(event):
    return {
        "owner_id": event["owner"]["id"],
        "owner_login": event["owner"]["login"],
        "distinct_id": event["owner"]["login"],
        "full_name": event["full_name"],
        "timestamp": event["created_at"]
    }


def main():
    run_script("vnd.github+json", "forks", "gh_forks", extract_data)


if __name__ == "__main__":
    main()
