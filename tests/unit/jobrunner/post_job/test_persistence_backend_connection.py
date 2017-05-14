from jobrunner.post_job import persistence_backend_connection
from jobrunner.settings import PERSISTENCE_CONF
from tests.testcase import TestCase


class TestPersistenceBackendConnection(TestCase):
    def setUp(self):
        self.fetch = self.set_up_patch(
            'jobrunner.post_job.persistence_backends.fetch'
        )

    def test_persistence_backend_connection_fetches_backend(self):
        self.assertFalse(self.fetch.called)

        with persistence_backend_connection():
            self.fetch.assert_called_once_with(PERSISTENCE_CONF)

    def test_persistence_backend_connection_yields_connection_to_context(self):
        with persistence_backend_connection() as conn:
            expected_connection = self.fetch.return_value.\
                get_connection.return_value
            self.assertEqual(conn, expected_connection)

    def test_persistence_backend_connection_closes_connection_after_ctx(self):
        with persistence_backend_connection() as conn:
            self.assertFalse(conn.close.called)

        conn.close.assert_called_once_with()
