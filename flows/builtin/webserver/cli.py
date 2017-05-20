from argparse import ArgumentParser

from flows.builtin.webserver.post import run_webserver
from jobrunner.cli.parse import parse_arguments
from jobrunner.jobs import register_job


def parse_webserver_arguments(args=None):
    """
    Parse the commandline options for posting a job that
    runs a simple HTTP webserver
    :param list args: Args to pass to the arg parser.
    Will use argv if none specified.
    :return obj args: parsed arguments
    """
    parser = ArgumentParser(
        prog="jobrunner post simple_http_webserver",
        description='Post a job that runs a simple HTTP webserver'
    )
    parser.add_argument(
        '--port', '-p', type=int, default=8080,
        help="The port to use to run the webserver on. Defaults to 8080"
    )
    return parse_arguments(parser, args=args)


@register_job()
def simple_http_webserver(args=None):
    """
    Show information about running jobs
    :param list args: Args to pass to the arg parser.
    Will use argv if none specified.
    :return None:
    """
    args = parse_webserver_arguments(args=args)
    run_webserver(port=args.port)
