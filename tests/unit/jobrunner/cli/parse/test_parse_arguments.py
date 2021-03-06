from mock import Mock, call

from jobrunner.cli.parse import parse_arguments
from tests.testcase import TestCase


class TestParseArguments(TestCase):
    def setUp(self):
        self.parser = Mock()
        self.setup_logging = self.set_up_patch('jobrunner.cli.parse.setup_logging')

    def test_parse_arguments_adds_arguments(self):
        parse_arguments(self.parser)

        expected_calls = [
            call('--verbose', '-v', action='store_true')
        ]
        self.assertEqual(
            self.parser.add_argument.mock_calls,
            expected_calls
        )

    def test_parse_arguments_parses_arguments(self):
        parse_arguments(self.parser)

        self.parser.parse_args.assert_called_once_with(
            args=None
        )

    def test_parse_arguments_parses_passed_args(self):
        expected_args = ['these', '--are', 'some_args']
        parse_arguments(self.parser, args=expected_args)

        self.parser.parse_args.assert_called_once_with(
            args=expected_args
        )

    def test_parse_arguments_sets_up_logging(self):
        parse_arguments(self.parser)

        self.setup_logging.assert_called_once_with(
            debug=self.parser.parse_args.return_value.verbose
        )

    def test_parse_arguments_returns_arguments(self):
        ret = parse_arguments(self.parser)

        self.assertEqual(ret, self.parser.parse_args.return_value)
