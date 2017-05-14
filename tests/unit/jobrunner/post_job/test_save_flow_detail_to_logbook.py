from mock import Mock

from jobrunner.post_job import save_flow_detail_to_logbook
from tests.testcase import TestCase


class TestSaveFlowDetailToLogbook(TestCase):
    def setUp(self):
        self.flow_detail = Mock()
        self.logbook = Mock()
        self.persistence_backend_connection = self.set_up_patch(
            'jobrunner.post_job.persistence_backend_connection'
        )
        self.persistence_backend_connection.return_value \
            .__exit__ = lambda a, b, c, d: None
        self.connection = Mock()
        self.persistence_backend_connection.return_value \
            .__enter__ = lambda x: self.connection

    def test_save_flow_detail_to_logbook_adds_flow_detail_to_logbook(self):
        save_flow_detail_to_logbook(
            self.flow_detail, self.logbook
        )

        self.logbook.add.assert_called_once_with(
            self.flow_detail
        )

    def test_save_flow_detail_to_logbook_gets_persist_backend_conn(self):
        save_flow_detail_to_logbook(
            self.flow_detail, self.logbook
        )

        self.persistence_backend_connection.assert_called_once_with()

    def test_save_flow_detail_to_logbook_saves_lb_to_persist_backend(self):
        save_flow_detail_to_logbook(
            self.flow_detail, self.logbook
        )

        self.connection.save_logbook.assert_called_once_with(
            self.logbook
        )
