from flows.builtin.helpers.parser import flow_parser
from tests.testcase import TestCase


class TestFlowParser(TestCase):
    def setUp(self):
        self.argument_parser = self.set_up_patch(
            'flows.builtin.helpers.parser.ArgumentParser'
        )
        self.flow_parser = self.set_up_patch(
            'flows.builtin.helpers.parser.flow_parser'
        )

    def test_flow_parser_instantiates_argparser(self):
        flow_parser(
            prog='jobrunner post simple_http_webserver',
            description='Post a job that runs a simple HTTP webserver'
        )

        self.argument_parser.assert_called_once_with(
            prog='jobrunner post simple_http_webserver',
            description='Post a job that runs a simple HTTP webserver'
        )

    def test_flow_parser_adds_hierarchy_argument(self):
        flow_parser()

        self.argument_parser.return_value.add_argument.assert_called_once_with(
            '--hierarchy', action='store_true',
            help="Print the execution graph of the flow that would be posted"
        )

    def test_flow_parser_returns_parser(self):
        ret = flow_parser()

        self.assertEqual(
            ret, self.argument_parser.return_value
        )
