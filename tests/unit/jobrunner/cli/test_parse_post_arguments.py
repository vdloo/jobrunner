from jobrunner.cli import parse_post_arguments
from tests.testcase import TestCase


class TestParsePostArguments(TestCase):
    def setUp(self):
        self.argument_parser = self.set_up_patch('jobrunner.cli.ArgumentParser')
        self.parse_arguments = self.set_up_patch('jobrunner.cli.parse_arguments')

    def test_parse_post_arguments_instantiates_argparser(self):
        parse_post_arguments()

        self.argument_parser.assert_called_once_with(
            prog='jobrunner post',
            description='Post a job to the jobboard'
        )

    def test_parse_post_arguments_adds_no_arguments(self):
        parse_post_arguments()

        self.assertFalse(
            self.argument_parser.return_value.add_argument.called
        )

    def test_parse_post_arguments_parses_arguments(self):
        parse_post_arguments()

        self.parse_arguments.assert_called_once_with(
            self.argument_parser.return_value
        )

    def test_parse_post_arguments_returns_parsed_arguments(self):
        ret = parse_post_arguments()

        self.assertEqual(
            ret, self.parse_arguments.return_value
        )
