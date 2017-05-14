from mock import Mock

from jobrunner.post_job import jobboard_backend_connection
from jobrunner.settings import CONDUCTOR_NAME
from jobrunner.settings import JOBBOARD_CONF
from tests.testcase import TestCase


class TestJobboardBackendConnection(TestCase):
    def setUp(self):
        self.persistence_backend = Mock()
        self.fetch = self.set_up_patch(
            'jobrunner.post_job.jobboard_backends.fetch'
        )

    def test_jobboard_backend_connection_fetches_backend(self):
        self.assertFalse(self.fetch.called)

        with jobboard_backend_connection(self.persistence_backend):
            self.fetch.assert_called_once_with(
                CONDUCTOR_NAME, JOBBOARD_CONF,
                persistence=self.persistence_backend
            )

    def test_jobboard_backend_connection_yields_connection_to_context(self):
        with jobboard_backend_connection(self.persistence_backend) as conn:
            expected_connection = self.fetch.return_value.\
                connect.return_value
            self.assertEqual(conn, expected_connection)

    def test_jobboard_backend_connection_closes_connection_after_ctx(self):
        with jobboard_backend_connection(self.persistence_backend) as conn:
            self.assertFalse(conn.close.called)

        conn.close.assert_called_once_with()
