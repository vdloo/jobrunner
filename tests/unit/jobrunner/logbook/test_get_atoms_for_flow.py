from mock import Mock
from tests.testcase import TestCase

from jobrunner.logbook import get_atoms_for_flow


class TestGetAtomsForFLow(TestCase):
    def setUp(self):
        self.flow = Mock()
        self.persistence_backend = Mock()

    def test_get_atoms_for_flow_gets_atoms_for_flow(self):
        get_atoms_for_flow(self.flow, self.persistence_backend)

        self.persistence_backend.get_atoms_for_flow.assert_called_once_with(
            self.flow.uuid
        )

    def test_get_flows_from_logbook_returns_flows(self):
        ret = get_atoms_for_flow(self.flow, self.persistence_backend)

        self.assertEqual(
            ret, self.persistence_backend.get_atoms_for_flow.return_value
        )

