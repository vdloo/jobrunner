from argparse import ArgumentParser

from jobrunner.cli.parse import parse_arguments
from jobrunner.show_logbook import show_logbook


def parse_show_arguments():
    """
    Parse the commandline options for showing running jobs
    :return obj args: parsed arguments
    """
    parser = ArgumentParser(
        prog="jobrunner show",
        description='Show information about running jobs'
    )
    return parse_arguments(parser)


def show():
    """
    Show information about running jobs
    :return None:
    """
    parse_show_arguments()
    show_logbook()
