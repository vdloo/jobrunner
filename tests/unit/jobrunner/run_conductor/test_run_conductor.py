from mock import Mock

from jobrunner.run_conductor import run_conductor
from jobrunner.settings import PERSISTENCE_CONF
from tests.testcase import TestCase


class TestRunConductor(TestCase):
    def setUp(self):
        self.log = self.set_up_patch(
            'jobrunner.run_conductor.log'
        )
        self.jobboard_backend_connection = self.set_up_patch(
            'jobrunner.run_conductor.jobboard_backend_connection'
        )
        self.jobboard_backend_connection.return_value \
            .__exit__ = lambda a, b, c, d: None
        self.j_connection = Mock()
        self.jobboard_backend_connection.return_value \
            .__enter__ = lambda x: self.j_connection
        self.persistence_fetch = self.set_up_patch(
            'jobrunner.run_conductor.persistence_backends.fetch'
        )
        self.start_conductor = self.set_up_patch(
            'jobrunner.run_conductor.start_conductor'
        )

    def test_run_conductor_gets_jobboard_backend_connection(self):
        run_conductor()

        self.jobboard_backend_connection.assert_called_once_with()

    def test_run_conductor_fetches_persistence_backend(self):
        run_conductor()

        self.persistence_fetch.assert_called_once_with(
            PERSISTENCE_CONF
        )

    def test_run_conductor_starts_conductor_with_the_configured_backends(self):
        run_conductor()

        self.start_conductor.assert_called_once_with(
            self.persistence_fetch.return_value, self.j_connection
        )
