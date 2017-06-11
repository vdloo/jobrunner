from jobrunner.iterator import has_capability
from jobrunner.plugins import register_capability
from jobrunner.settings import CAPABILITIES
from tests.testcase import TestCase


class TestHasCapability(TestCase):
    def setUp(self):
        to_del = (
            'does_not_exist',
            'registered_and_evaluates_to_true',
            'registered_and_evaluates_to_false'
        )
        for capability in to_del:
            if capability in CAPABILITIES:
                del CAPABILITIES[capability]

        @register_capability()
        def registered_and_evaluates_to_true():
            return True

        @register_capability()
        def registered_and_evaluates_to_false():
            return False

    def test_has_capability_returns_false_if_capability_not_registered(self):
        ret = has_capability('does_not_exist')

        self.assertFalse(ret)

    def test_has_capability_returns_true_if_registered_and_returns_true(self):
        ret = has_capability('registered_and_evaluates_to_true')

        self.assertTrue(ret)

    def test_has_capability_returns_false_if_registered_and_returns_false(self):
        ret = has_capability('registered_and_evaluates_to_false')

        self.assertFalse(ret)
