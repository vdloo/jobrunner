from uuid import uuid4

from mock import Mock

from jobrunner.logbook import get_flow_details_by_uuid
from tests.testcase import TestCase


class TestGetFlowDetailsByUuid(TestCase):
    def setUp(self):
        self.flow_uuid = str(uuid4())
        self.persistence_backend_connection = self.set_up_patch(
            'jobrunner.logbook.persistence_backend_connection'
        )
        self.persistence_backend_connection.return_value \
            .__exit__ = lambda a, b, c, d: None
        self.connection = Mock()
        self.persistence_backend_connection.return_value \
            .__enter__ = lambda x: self.connection

    def test_get_flow_details_by_uuid_gets_persistence_backend_conn(self):
        get_flow_details_by_uuid(self.flow_uuid)

        self.persistence_backend_connection.assert_called_once_with()

    def test_get_flow_details_by_uuid_gets_flow_details_from_p_backend(self):
        get_flow_details_by_uuid(self.flow_uuid)

        self.connection.get_flow_details.assert_called_once_with(
            self.flow_uuid
        )

    def test_get_flow_details_by_uuid_returns_flow_details(self):
        ret = get_flow_details_by_uuid(self.flow_uuid)

        self.assertEqual(
            ret, self.connection.get_flow_details.return_value
        )
