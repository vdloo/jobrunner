from jobrunner.cli.run import parse_run_arguments
from tests.testcase import TestCase


class TestParseRunArguments(TestCase):
    def setUp(self):
        self.argument_parser = self.set_up_patch('jobrunner.cli.run.ArgumentParser')
        self.parse_arguments = self.set_up_patch('jobrunner.cli.run.parse_arguments')

    def test_parse_run_arguments_instantiates_argparser(self):
        parse_run_arguments()

        self.argument_parser.assert_called_once_with(
            prog='jobrunner run',
            description='Run a conductor which processes jobs'
        )

    def test_parse_run_arguments_adds_no_arguments(self):
        parse_run_arguments()

        self.assertFalse(
            self.argument_parser.return_value.add_argument.called
        )

    def test_parse_run_arguments_parses_arguments(self):
        parse_run_arguments()

        self.parse_arguments.assert_called_once_with(
            self.argument_parser.return_value
        )

    def test_parse_run_arguments_returns_parsed_arguments(self):
        ret = parse_run_arguments()

        self.assertEqual(
            ret, self.parse_arguments.return_value
        )
