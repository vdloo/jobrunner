from mock import Mock

from jobrunner.post_job import get_logbook_by_name
from tests.testcase import TestCase


class TestGetLogBookByName(TestCase):
    def setUp(self):
        self.connection = Mock()
        self.mock_logbook_1 = Mock()
        self.mock_logbook_1.name = 'logbook1'
        self.mock_logbook_2 = Mock()
        self.mock_logbook_2.name = 'logbook2'
        self.connection.get_logbooks.return_value = (
            self.mock_logbook_1, self.mock_logbook_2
        )

    def test_get_logbook_by_name_gets_logbooks_from_connection(self):
        get_logbook_by_name('logbook1', self.connection)

        self.connection.get_logbooks.assert_called_once_with()

    def test_get_logbook_by_name_raises_stop_iteration_if_no_such_lb(self):
        with self.assertRaises(StopIteration):
            get_logbook_by_name('logbook0', self.connection)

    def test_get_logbook_by_name_returns_logbook_1_by_name(self):
        ret = get_logbook_by_name('logbook1', self.connection)

        self.assertEqual(ret, self.mock_logbook_1)

    def test_get_logbook_by_name_returns_logbook_2_by_name(self):
        ret = get_logbook_by_name('logbook2', self.connection)

        self.assertEqual(ret, self.mock_logbook_2)

    def test_get_logbook_by_name_returns_first_logbook_if_more_with_name(self):
        mock_logbook_3 = Mock()
        mock_logbook_3.name = 'logbook1'
        self.connection.get_logbooks.return_value = (
            self.mock_logbook_1, mock_logbook_3
        )

        ret = get_logbook_by_name('logbook1', self.connection)

        self.assertEqual(ret, self.mock_logbook_1)
