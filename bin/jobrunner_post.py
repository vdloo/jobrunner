#!/usr/bin/env python3
from jobrunner.cli.post import post

if __name__ == '__main__':
    post()
else:
    raise RuntimeError("This script is an entry point and can not be imported")
