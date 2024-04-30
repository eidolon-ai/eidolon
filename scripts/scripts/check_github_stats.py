import argparse
import json
import os


def parse_repohistory_data():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repohistory_data.json')) as f:
        data = json.load(f)

    tmp = [arr[3] for arr in json.loads(data[1][3:])]
    print(data)


def main():
    parse_repohistory_data()


if __name__ == "__main__":
    main()
