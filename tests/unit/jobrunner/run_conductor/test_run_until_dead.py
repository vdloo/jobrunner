from mock import Mock, ANY
from tests.testcase import TestCase

from jobrunner.run_conductor import run_until_dead


class TestRunUntilDead(TestCase):
    def setUp(self):
        self.conductor = Mock()
        self.log = self.set_up_patch(
            'jobrunner.run_conductor.log'
        )

    def test_run_until_dead_logs_debug_message(self):
        run_until_dead(self.conductor)

        self.log.debug.assert_called_once_with(ANY)

    def test_run_until_dead_runs_conductor(self):
        run_until_dead(self.conductor)

        self.conductor.run.assert_called_once_with()

    def test_run_until_dead_stops_conductor(self):
        run_until_dead(self.conductor)

        self.conductor.stop.assert_called_once_with()

    def test_run_until_dead_stops_conductor_after_error_also(self):
        self.conductor.run.side_effect = Exception

        with self.assertRaises(Exception):
            run_until_dead(self.conductor)

        self.conductor.stop.assert_called_once_with()

    def test_run_until_dead_waits_for_jobs_to_finish(self):
        run_until_dead(self.conductor)

        self.conductor.wait.assert_called_once_with()

    def test_run_until_dead_waits_for_jobs_to_finish_after_error_also(self):
        self.conductor.wait.side_effect = Exception

        with self.assertRaises(Exception):
            run_until_dead(self.conductor)

        self.conductor.wait.assert_called_once_with()
