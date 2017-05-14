from mock import Mock
from tests.testcase import TestCase

from jobrunner.show_logbook import get_logbooks


class TestGetLogbooks(TestCase):
    def setUp(self):
        self.persistence_backend = Mock()

    def test_get_logbooks_gets_logbooks_from_persistence_backend(self):
        get_logbooks(self.persistence_backend)

        self.persistence_backend.get_logbooks.assert_called_once_with()

    def test_get_logbooks_returns_logbooks(self):
        ret = get_logbooks(self.persistence_backend)

        self.assertEqual(
            ret, self.persistence_backend.get_logbooks.return_value
        )
