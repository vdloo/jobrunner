from mock import Mock

from jobrunner.post_job import ensure_logbook_exists
from jobrunner.settings import LOGBOOK_NAME
from tests.testcase import TestCase


class TestEnsureLogbookExists(TestCase):
    def setUp(self):
        self.log = self.set_up_patch(
            'jobrunner.post_job.log'
        )
        self.persistence_backend_connection = self.set_up_patch(
            'jobrunner.post_job.persistence_backend_connection'
        )
        self.persistence_backend_connection.return_value\
            .__exit__ = lambda a, b, c, d: None
        self.connection = Mock()
        self.persistence_backend_connection.return_value\
            .__enter__ = lambda x: self.connection
        self.get_logbook_by_name = self.set_up_patch(
            'jobrunner.post_job.get_logbook_by_name'
        )
        self.LogBook = self.set_up_patch(
            'jobrunner.post_job.persistence_models.LogBook'
        )

    def test_ensure_logbook_exists_logs_debug_message(self):
        ensure_logbook_exists()

        self.assertTrue(self.log.debug.called)

    def test_ensure_logbook_exists_gets_persistence_backend_connection(self):
        ensure_logbook_exists()

        self.persistence_backend_connection.assert_called_once_with()

    def test_ensure_logbook_upgrades_the_persistence_backend_if_needed(self):
        ensure_logbook_exists()

        self.connection.upgrade.assert_called_once_with()

    def test_ensure_logbook_gets_logbook_by_name_from_connection(self):
        ensure_logbook_exists()

        self.get_logbook_by_name.assert_called_once_with(
            LOGBOOK_NAME, self.connection
        )

    def test_ensure_logbook_does_not_instantiate_new_logbook_if_exists(self):
        ensure_logbook_exists()

        self.assertFalse(self.LogBook.called)

    def test_ensure_logbook_does_not_save_logbook_if_exists(self):
        ensure_logbook_exists()

        self.assertFalse(self.connection.save_logbook.called)

    def test_ensure_logbook_instantiates_new_logbook_if_did_not_exist(self):
        self.get_logbook_by_name.side_effect = StopIteration

        ensure_logbook_exists()

        self.LogBook.assert_called_once_with(LOGBOOK_NAME)

    def test_ensure_logbook_saves_new_logbook_if_did_not_exist(self):
        self.get_logbook_by_name.side_effect = StopIteration

        ensure_logbook_exists()

        self.connection.save_logbook.assert_called_once_with(
            self.LogBook.return_value
        )
