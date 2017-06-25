from sys import argv

from jobrunner.plugins import load_all_plugins
from jobrunner.settings import JOBS

POST_HELP_MENU = """
usage: jobrunner post [-h] [--verbose] {{job_name}}

Post a job to the job board

available jobs:
  {}
                        The job to post

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v

"""


def print_post_help():
    """
    Print the post help menu, listing all available jobs
    :return None:
    """
    # Hardcoded help menu because you can't run argparser twice
    # the post command runs any of the registered jobs functions
    # which should all implement an argparser themselves for job
    # specific options.
    print(POST_HELP_MENU.format('\n  '.join(JOBS.keys())))


def post():
    """
    Post a job to the job board based on commandline arguments
    :return None:
    """
    load_all_plugins()
    if len(argv) < 2 or argv[1] not in JOBS.keys():
        print_post_help()
    else:
        JOBS[argv[1]](argv[2:])
