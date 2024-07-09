import argparse
import json
import os
from pydantic import validate_call
from typing import Literal

from scripts.version_poetry_project import rev_version


@validate_call
def update_path_deps(version: Literal['major', 'minor', 'patch']):
    loc = "k8s-operator"
    print(f"Checking for updates: {loc}")
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    with open(os.path.join(loc, 'env.json')) as f:
        data = json.load(f)
        updated_version = rev_version(data['version'], version)
        data['version'] = updated_version
        with open(os.path.join(loc, 'env.json'), 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated version to {updated_version}")


def main():
    parser = argparse.ArgumentParser(description="Get path dependencies from a poetry project")
    parser.add_argument("--version", default='patch', help="major, minor, or patch")
    update_path_deps(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
