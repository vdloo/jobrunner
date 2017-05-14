from mock import Mock

from jobrunner.post_job import jobboard_backend_connection
from jobrunner.settings import CONDUCTOR_NAME, PERSISTENCE_CONF
from jobrunner.settings import JOBBOARD_CONF
from tests.testcase import TestCase


class TestJobboardBackendConnection(TestCase):
    def setUp(self):
        self.persistence_fetch = self.set_up_patch(
            'jobrunner.post_job.persistence_backends.fetch'
        )
        self.job_board_fetch = self.set_up_patch(
            'jobrunner.post_job.jobboard_backends.fetch'
        )

    def test_jobboard_backend_connection_fetches_persistence_backend(self):
        self.assertFalse(self.persistence_fetch.called)

        with jobboard_backend_connection():
            self.persistence_fetch.assert_called_once_with(
                PERSISTENCE_CONF
            )

    def test_jobboard_backend_connection_fetches_job_board_backend(self):
        self.assertFalse(self.job_board_fetch.called)

        with jobboard_backend_connection():
            self.job_board_fetch.assert_called_once_with(
                CONDUCTOR_NAME, JOBBOARD_CONF,
                persistence=self.persistence_fetch.return_value
            )

    def test_jobboard_backend_connection_connects_to_jobboard(self):
        self.assertFalse(self.job_board_fetch.return_value.connect.called)
        with jobboard_backend_connection():
            self.job_board_fetch.return_value.connect.assert_called_once_with()

    def test_jobboard_backend_connection_yields_connection_to_context(self):
        with jobboard_backend_connection() as conn:
            expected_connection = self.job_board_fetch.return_value
            self.assertEqual(conn, expected_connection)

    def test_jobboard_backend_connection_closes_connection_after_ctx(self):
        with jobboard_backend_connection() as conn:
            self.assertFalse(conn.close.called)

        conn.close.assert_called_once_with()
