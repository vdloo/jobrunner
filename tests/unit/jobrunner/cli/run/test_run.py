from jobrunner.cli.run import run
from tests.testcase import TestCase


class TestRun(TestCase):
    def setUp(self):
        self.parse_run_arguments = self.set_up_patch(
            'jobrunner.cli.run.parse_run_arguments'
        )
        self.run_conductor = self.set_up_patch(
            'jobrunner.cli.run.run_conductor'
        )

    def test_run_parses_run_arguments(self):
        run()

        self.parse_run_arguments.assert_called_once_with()

    def test_run_runs_conductor(self):
        run()

        self.run_conductor.assert_called_once_with()
