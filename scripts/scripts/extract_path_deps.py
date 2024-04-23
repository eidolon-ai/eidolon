import argparse
import toml
import os


def extract_path_deps(loc, workdir, suffix):
    if workdir:
        os.chdir(workdir)
    data = toml.load(os.path.join(loc, 'pyproject.toml'))
    deps = data.get('tool', {}).get('poetry', {}).get('group', {}).get("dev", {}).get("dependencies", {})
    path_deps = [(dep, details['path']) for dep, details in deps.items() if isinstance(details, dict) and 'path' in details]
    print(' '.join([os.path.normpath(os.path.join(loc, path, suffix or "")) for dep, path in path_deps]))


def main():
    parser = argparse.ArgumentParser(description="Get path dependencies from a poetry project")
    parser.add_argument("--loc", required=False, help="project location", default=".")
    parser.add_argument("--workdir", required=False, help="working directory", default=None)
    parser.add_argument("--suffix", required=False, help="suffix to add to the path", default=None)
    extract_path_deps(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
