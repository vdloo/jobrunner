from jobrunner.cli import show
from tests.testcase import TestCase


class TestShow(TestCase):
    def setUp(self):
        self.parse_show_arguments = self.set_up_patch(
            'jobrunner.cli.parse_show_arguments'
        )
        self.show_logbook = self.set_up_patch(
            'jobrunner.cli.show_logbook'
        )

    def test_show_parses_show_arguments(self):
        show()

        self.parse_show_arguments.assert_called_once_with()

    def test_show_shows_logbooks(self):
        show()

        self.show_logbook.assert_called_once_with()
