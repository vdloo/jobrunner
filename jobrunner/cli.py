from argparse import ArgumentParser

from jobrunner.log import setup_logging
from jobrunner.post_job import post_job
from jobrunner.run_conductor import run_conductor


def parse_arguments(parser):
    """
    Add default parser arguments to parser and parse arguments. Also sets logging level.
    :param obj parser:
    :return obj args: parsed arguments
    """
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    setup_logging(debug=args.verbose)
    return args


def parse_post_arguments():
    """
    Parse the commandline options for posting a job to the job board
    :return obj args: parsed arguments
    """
    parser = ArgumentParser(
        prog="jobrunner post",
        description='Post a job to the job board'
    )
    return parse_arguments(parser)


def post():
    """
    Post a job to the job board based on commandline arguments
    :return None:
    """
    parse_post_arguments()
    post_job()


def parse_run_arguments():
    """
    Parse the commandline options for running the conductor
    :return obj args: parsed arguments
    """
    parser = ArgumentParser(
        prog="jobrunner run",
        description='Run a conductor which processes jobs'
    )
    return parse_arguments(parser)


def run():
    """
    Run a conductor to process jobs on the job board
    :return None:
    """
    parse_run_arguments()
    run_conductor()
