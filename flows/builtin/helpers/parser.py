from argparse import ArgumentParser


def flow_parser(prog=None, description=None):
    """
    Create a standard jobrunner argument parser
    :param str prog: Name of the prog
    :param str description: Description of the prog
    :return:
    """
    parser = ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '--hierarchy', action='store_true',
        help="Print the execution graph of the flow that would be posted"
    )
    return parser

