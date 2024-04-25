import argparse
import json
import os
from typing import Literal

from git import Repo
from pydantic import validate_call

from scripts.version_poetry_project import changed_since_commit, rev_version


@validate_call
def update_path_deps(loc: str, version: Literal['major', 'minor', 'patch']):
    print(f"Checking for updates: {loc}")
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    with open(os.path.join(loc, 'package.json')) as f:
        data = json.load(f)

    if changed_since_commit(data.setdefault('eidolon', {}).get('last-update-hash'), loc):
        data['eidolon']['last-update-hash'] = Repo(".").head.commit.hexsha
        updated_version = rev_version(data['version'], version)
        data['version'] = updated_version
        with open(os.path.join(loc, 'package.json'), 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated version to {updated_version}")
    else:
        print("No changes detected")


def main():
    parser = argparse.ArgumentParser(description="Get path dependencies from a poetry project")
    parser.add_argument("loc", help="project location")
    parser.add_argument("--version", default='patch', help="major, minor, or patch")
    update_path_deps(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
