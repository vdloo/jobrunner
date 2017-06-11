from mock import Mock

from jobrunner.iterator import has_capability
from jobrunner.plugins import register_capability
from jobrunner.settings import CAPABILITIES
from tests.testcase import TestCase


class TestHasCapability(TestCase):
    def setUp(self):
        self.job = Mock()
        to_del = (
            'does_not_exist',
            'registered_and_evaluates_to_true',
            'registered_and_evaluates_to_false',
            'check_if_arg_is_job'
        )
        for capability in to_del:
            if capability in CAPABILITIES:
                del CAPABILITIES[capability]

        @register_capability()
        def registered_and_evaluates_to_true(_):
            return True

        @register_capability()
        def registered_and_evaluates_to_false(_):
            return False

        @register_capability()
        def check_if_arg_is_job(job):
            self.assertEqual(job, self.job)
            return True

    def test_has_capability_returns_false_if_capability_not_registered(self):
        ret = has_capability(
            'does_not_exist', jobboard_job=self.job
        )

        self.assertFalse(ret)

    def test_has_capability_returns_true_if_registered_and_returns_true(self):
        ret = has_capability(
            'registered_and_evaluates_to_true', jobboard_job=self.job
        )

        self.assertTrue(ret)

    def test_has_capability_returns_false_if_registered_and_returns_false(self):
        ret = has_capability(
            'registered_and_evaluates_to_false', jobboard_job=self.job
        )

        self.assertFalse(ret)

    def test_has_capability_passes_job_as_arg_to_capability_checker(self):
        ret = has_capability(
            'check_if_arg_is_job', jobboard_job=self.job
        )
