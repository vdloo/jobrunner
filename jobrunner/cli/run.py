from argparse import ArgumentParser

from jobrunner.cli.parse import parse_arguments
from jobrunner.run_conductor import run_conductor


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
