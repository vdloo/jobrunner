from mock import ANY

from flows.builtin.webserver.cli import parse_webserver_arguments
from tests.testcase import TestCase


class TestParseWebserverArguments(TestCase):
    def setUp(self):
        self.argument_parser = self.set_up_patch(
            'flows.builtin.webserver.cli.ArgumentParser'
        )
        self.parse_arguments = self.set_up_patch(
            'flows.builtin.webserver.cli.parse_arguments'
        )

    def test_parse_webserver_arguments_instantiates_argparser(self):
        parse_webserver_arguments()

        self.argument_parser.assert_called_once_with(
            prog='jobrunner post simple_http_webserver',
            description='Post a job that runs a simple HTTP webserver'
        )

    def test_parse_webserver_arguments_adds_port_argument(self):
        parse_webserver_arguments()

        self.argument_parser.return_value.add_argument.assert_called_once_with(
            '--port', '-p', type=int, default=8080,
            help=ANY
        )

    def test_parse_webserver_arguments_parses_arguments(self):
        parse_webserver_arguments()

        self.parse_arguments.assert_called_once_with(
            self.argument_parser.return_value, args=None
        )

    def test_parse_webserver_arguments_parses_specified_arguments(self):
        expected_args = ['these', '--are', 'some_args']

        parse_webserver_arguments(args=expected_args)

        self.parse_arguments.assert_called_once_with(
            self.argument_parser.return_value, args=expected_args
        )

    def test_parse_webserver_arguments_returns_parsed_arguments(self):
        ret = parse_webserver_arguments()

        self.assertEqual(
            ret, self.parse_arguments.return_value
        )
