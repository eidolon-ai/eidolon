import argparse
from typing import Literal

import toml
import os
from pydantic import validate_call

from git import Repo


@validate_call
def update_path_deps(loc: str, version: Literal['major', 'minor', 'patch']):
    print(f"Checking for updates: {loc}")

    os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    data = toml.load(os.path.join(loc, 'pyproject.toml'))
    deps = data.get('tool', {}).get('poetry', {}).get('group', {}).get("dev", {}).get("dependencies", {})
    changed = False

    for dep, dep_info in deps.items():
        if isinstance(dep_info, dict) and 'path' in dep_info:
            path = dep_info['path']
            dep_data = toml.load(os.path.join(loc, path, 'pyproject.toml'))
            existing_version = dep_data['tool']['poetry']['version']

            desired_version = "^" + existing_version
            if data['tool']['poetry']['dependencies'][dep] != desired_version:
                print(f"...dependency {dep} updated to {desired_version}")
                data['tool']['poetry']['dependencies'][dep] = desired_version
                changed = True

    repo = Repo(".")
    eidolon_tool = data.setdefault('tool', {}).setdefault('eidolon', {})
    last_update_hash = eidolon_tool.get('last-update-hash')
    last_relevant_hash = get_next_commit(repo, last_update_hash) if last_update_hash else None
    if not last_relevant_hash:
        print("...last-update-hash found")
        changed = True
    else:
        # check diff between last relevant hash and current hash
        commit = repo.commit(last_relevant_hash)
        diff = commit.diff('HEAD', paths=loc)
        for item in diff:
            print(f"...file {item.a_path} changed")
            changed = True
            break

    if changed:
        eidolon_tool['last-update-hash'] = repo.head.commit.hexsha
        updated_version = method_name(data['tool']['poetry']['version'], version)
        data['tool']['poetry']['version'] = updated_version
        with open(os.path.join(loc, 'pyproject.toml'), 'w') as f:
            toml.dump(data, f)
        print(f"Updated version to {updated_version}")
    else:
        print("No changes detected")


def method_name(current_version, rev_type):
    major, minor, patch = current_version.split('.')
    if rev_type == 'major':
        updated_version = f"{int(major) + 1}.0.0"
    elif rev_type == 'minor':
        updated_version = f"{major}.{int(minor) + 1}.0"
    elif rev_type == 'patch':
        updated_version = f"{major}.{minor}.{int(patch) + 1}"
    else:
        raise ValueError(f"Invalid version {rev_type}")
    return updated_version


def get_next_commit(repo: Repo, commit_hash):
    commits = repo.iter_commits(rev=commit_hash + "...")
    try:
        return list(commits)[-1]
    except IndexError:
        raise ValueError(f"Commit after {commit_hash} not found in repository, if you have local changes, please commit them")


def main():
    parser = argparse.ArgumentParser(description="Get path dependencies from a poetry project")
    parser.add_argument("loc", help="project location")
    parser.add_argument("--version", default='patch', help="major, minor, or patch")
    update_path_deps(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
