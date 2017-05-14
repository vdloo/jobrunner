from mock import Mock, ANY

from jobrunner.run_conductor import start_conductor, log_conductor_event
from jobrunner.settings import CONDUCTOR_NAME
from tests.testcase import TestCase


class TestStartConductor(TestCase):
    def setUp(self):
        self.persistence_backend = Mock()
        self.job_backend = Mock()
        self.log = self.set_up_patch(
            'jobrunner.run_conductor.log'
        )
        self.conductor_fetch = self.set_up_patch(
            'jobrunner.run_conductor.conductor_backends.fetch'
        )
        self.conductor = self.conductor_fetch.return_value
        self.run_until_dead = self.set_up_patch(
            'jobrunner.run_conductor.run_until_dead'
        )

    def test_start_conductor_logs_info_message(self):
        start_conductor(self.persistence_backend, self.job_backend)

        self.log.info.assert_called_once_with(ANY)

    def test_start_conductor_fetches_conductor_backend(self):
        start_conductor(self.persistence_backend, self.job_backend)

        self.conductor_fetch.asssert_called_once_with(
            'noblocking', CONDUCTOR_NAME, self.job_backend,
            persistence=self.persistence_backend
        )

    def test_start_conductor_registers_log_conductor_event_notifier(self):
        start_conductor(self.persistence_backend, self.job_backend)

        self.conductor.notifier.register.assert_called_once_with(
            self.conductor.notifier.ANY, log_conductor_event
        )

    def test_start_conductor_runs_the_conductor_until_dead(self):
        start_conductor(self.persistence_backend, self.job_backend)

        self.run_until_dead.assert_called_once_with(self.conductor)
