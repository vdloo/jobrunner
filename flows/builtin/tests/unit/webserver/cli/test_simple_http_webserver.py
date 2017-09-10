from flows.builtin.webserver.cli import simple_http_webserver
from tests.testcase import TestCase


class TestSimpleHttpWebserver(TestCase):
    def setUp(self):
        self.parse_webserver_arguments = self.set_up_patch(
            'flows.builtin.webserver.cli.parse_webserver_arguments'
        )
        self.run_webserver = self.set_up_patch(
            'flows.builtin.webserver.cli.run_webserver'
        )

    def test_simple_http_webserver_parses_webserver_args(self):
        simple_http_webserver()

        self.parse_webserver_arguments.assert_called_once_with(
            args=None
        )

    def test_simple_http_webserver_parses_specified_args(self):
        expected_args = ['these', '--are', 'some_args']

        simple_http_webserver(args=expected_args)

        self.parse_webserver_arguments.assert_called_once_with(
            args=expected_args
        )

    def test_simple_http_webserver_runs_webserver(self):
        simple_http_webserver()

        self.run_webserver.assert_called_once_with(
            port=self.parse_webserver_arguments.return_value.port,
            hierarchy=self.parse_webserver_arguments.return_value.hierarchy
        )
