#!/usr/bin/env python3
from jobrunner.cli import show

if __name__ == '__main__':
    show()
else:
    raise RuntimeError("This script is an entry point and can not be imported")
