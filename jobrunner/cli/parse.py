from jobrunner.log import setup_logging


def parse_arguments(parser, args=None):
    """
    Add default parser arguments to parser and parse arguments.
    Also sets logging level.
    :param obj parser:
    :param list args: Args to pass to the arg parser.
    Will use argv if none specified.
    :return obj args: parsed arguments
    """
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args(args=args)
    setup_logging(debug=args.verbose)
    return args
