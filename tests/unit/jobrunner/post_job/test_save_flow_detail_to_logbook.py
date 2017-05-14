from mock import Mock

from jobrunner.post_job import save_flow_detail_to_logbook
from tests.testcase import TestCase


class TestSaveFlowDetailToLogbook(TestCase):
    def setUp(self):
        self.flow_detail = Mock()
        self.logbook = Mock()
        self.job_backend = Mock()

    def test_save_flow_detail_to_logbook_adds_flow_detail_to_logbook(self):
        save_flow_detail_to_logbook(
            self.flow_detail, self.logbook, self.job_backend
        )

        self.logbook.add.assert_called_once_with(
            self.flow_detail
        )

    def test_save_flow_detail_to_logbook_saves_logbook_to_job_backend(self):
        save_flow_detail_to_logbook(
            self.flow_detail, self.logbook, self.job_backend
        )

        self.job_backend.save_logbook.assert_called_once_with(
            self.logbook
        )
