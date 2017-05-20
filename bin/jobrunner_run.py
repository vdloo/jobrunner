#!/usr/bin/env python3
from jobrunner.cli.run import run

if __name__ == '__main__':
    run()
else:
    raise RuntimeError("This script is an entry point and can not be imported")
