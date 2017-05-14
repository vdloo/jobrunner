from mock import Mock
from tests.testcase import TestCase

from jobrunner.show_logbook import get_flows_from_logbook


class TestGetFlowsFromLogbook(TestCase):
    def setUp(self):
        self.logbook = Mock()
        self.persistence_backend = Mock()

    def test_get_flows_from_logbook_gets_flows_from_logbook(self):
        get_flows_from_logbook(self.logbook, self.persistence_backend)

        self.persistence_backend.get_flows_for_book.assert_called_once_with(
            self.logbook.uuid
        )

    def test_get_flows_from_logbook_returns_flows(self):
        ret = get_flows_from_logbook(self.logbook, self.persistence_backend)

        self.assertEqual(
            ret, self.persistence_backend.get_flows_for_book.return_value
        )

