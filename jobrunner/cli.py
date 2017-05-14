from argparse import ArgumentParser

from jobrunner.log import setup_logging


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
    Parse the commandline options for posting a job to the jobboard
    :return obj args: parsed arguments
    """
    parser = ArgumentParser(
        prog="jobrunner post",
        description='Post a job to the jobboard'
    )
    return parse_arguments(parser)


def post():
    """
    Post a job to the jobboard
    :return None:
    """
    args = parse_post_arguments()
    # Does not post a job yet