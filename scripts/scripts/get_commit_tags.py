import os
from typing import Optional

from git import Repo
import toml


def get_project_tag(path) -> Optional[str]:
    # Load the pyproject.toml file
    with open(path, 'r') as file:
        pyproject = toml.load(file)

    # Get the project version
    version = pyproject['tool']['poetry']['version']
    tag = pyproject['tool'].get("eidolon", {}).get("update-tag")
    if tag:
        return f"{tag}/{version}"
    else:
        return None


def git_diff(repo):
    # Check for changes in the git repository
    diff = repo.git.diff('--name-only')
    # the next line splits diff on newline characters
    return diff.splitlines()


def git_commit(repo, commit_message):
    # Add all changes to the staging area
    repo.git.add(update=True)

    # Commit the changes
    repo.index.commit(commit_message)


def git_tag(repo, tag_name):
    # Tag the current commit
    repo.create_tag(tag_name)


def main():
    # the next line changes the working directory to the parent directory of this file
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    # Initialize the git repo
    repo = Repo('.')
    tags = []

    # Check if there are changes in the pyproject.toml file
    for file in git_diff(repo):
        # suffix = 'pyproject.toml'
        suffix = 'sdk/pyproject.toml'  # only single tag supported for now
        if file.endswith(suffix):
            tag = get_project_tag(file)
            if tag:
                tags.append(tag)

    print(" ".join(tags))


if __name__ == "__main__":
    main()
