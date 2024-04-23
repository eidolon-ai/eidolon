import argparse
import toml
import os


def update_path_deps(loc):
    data = toml.load(os.path.join(loc, 'pyproject.toml'))
    deps = data.get('tool', {}).get('poetry', {}).get('group', {}).get("dev", {}).get("dependencies", {})
    changed = False

    for dep, dep_info in deps.items():
        if isinstance(dep_info, dict) and 'path' in dep_info:
            path = dep_info['path']
            dep_data = toml.load(os.path.join(loc, path, 'pyproject.toml'))
            version = dep_data['tool']['poetry']['version']

            desired_version = "^" + version
            if data['tool']['poetry']['dependencies'][dep] != desired_version:
                print(f"Dependency {dep} updated to {desired_version}")
                data['tool']['poetry']['dependencies'][dep] = desired_version
                changed = True

    if changed:
        with open(os.path.join(loc, 'pyproject.toml'), 'w') as f:
            toml.dump(data, f)


def main():
    parser = argparse.ArgumentParser(description="Get path dependencies from a poetry project")
    parser.add_argument("loc", help="project location")
    update_path_deps(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
