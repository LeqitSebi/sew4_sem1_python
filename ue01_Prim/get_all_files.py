#!/usr/bin/python3.7

import os


def get_all_files(pathname):
    for path in os.listdir(pathname):
        abs_path = os.path.join(pathname, path)
        if os.path.isdir(abs_path):
            yield from get_all_files(abs_path)
        else:
            yield abs_path


for f in get_all_files('./'):
    print(f)

