#!/usr/bin/env python3

import argparse
import json
import mining


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login', help='VK login', required=True)
    parser.add_argument('-p', '--password', help='VK password', required=True)
    args = parser.parse_args()

    group_data = mining.load_posts(args.login, args.password)
    with open('data/group_data.json', 'w') as gr_data_file:
        json.dump(group_data, gr_data_file)


if __name__ == '__main__':
    main()