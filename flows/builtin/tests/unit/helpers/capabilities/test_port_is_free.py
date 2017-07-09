from uuid import uuid4
from mock import Mock, call

from tests.testcase import TestCase
from flows.builtin.helpers.capabilities import port_is_free, set_cached_port_is_free, \
    reset_cached_port_is_free_timestamp


class TestPortIsFree(TestCase):
    def setUp(self):
        self.time = self.set_up_patch(
            'flows.builtin.helpers.capabilities.time'
        )
        self.time.side_effect = (
            # Save time in global
            1497192855.084605,
            # Check time for the first time after setting globals
            1497192856.064605,
            # Second time is not saved in global because
            # it happens in the 10 second window
        )
        self.flow_uuid = str(uuid4())
        self.job = Mock(details={'flow_uuid': self.flow_uuid})
        self.check_nonzero_exit = self.set_up_patch(
            'flows.builtin.helpers.capabilities.check_nonzero_exit'
        )
        self.check_nonzero_exit.return_value = True
        self.get_flow_details_by_uuid = self.set_up_patch(
            'flows.builtin.helpers.capabilities.get_flow_details_by_uuid'
        )
        self.get_flow_details_by_uuid.return_value = Mock(
            meta={'store': {'port': 1234}}
        )
        # Reset the global memoized result every test method
        set_cached_port_is_free(None)
        reset_cached_port_is_free_timestamp()

    def test_port_is_free_gets_flow_details_for_job_uuid(self):
        port_is_free(self.job)

        self.get_flow_details_by_uuid.assert_called_once_with(
            self.flow_uuid
        )

    def test_port_is_free_checks_port_is_free(self):
        port_is_free(self.job)

        self.check_nonzero_exit.assert_called_once_with(
            'netstat -tuna | grep -q 1234'
        )

    def test_port_is_free_uses_cached_result_when_checking_twice(self):
        port_is_free(self.job)
        port_is_free(self.job)

        # Only once
        self.check_nonzero_exit.assert_called_once_with(
            'netstat -tuna | grep -q 1234'
        )

    def test_port_is_free_checks_again_if_port_was_free(self):
        set_cached_port_is_free(True)

        self.time.side_effect = (
            # Save time in global
            1497192855.084605,
            # Check time for the first time after setting globals
            1497192856.064605 + 10,
            # Save time in global, updating the first timestamp
            1497192856.084605 + 10,
        )

        port_is_free(self.job)
        port_is_free(self.job)

        expected_calls = [
            call('netstat -tuna | grep -q 1234')
        ] * 2
        self.assertCountEqual(
            expected_calls, self.check_nonzero_exit.mock_calls
        )

    def test_port_is_free_checks_again_after_ten_seconds(self):
        self.time.side_effect = (
            # Save time in global
            1497192855.084605,
            # Check time for the first time after setting globals
            1497192856.064605 + 10,
            # Save time in global, updating the first timestamp
            1497192856.084605 + 10,
        )

        port_is_free(self.job)
        port_is_free(self.job)

        expected_calls = [
            call('netstat -tuna | grep -q 1234')
        ] * 2
        self.assertCountEqual(
            expected_calls, self.check_nonzero_exit.mock_calls
        )

    def test_port_is_free_returns_true_if_port_is_free(self):
        self.check_nonzero_exit.return_value = False
        
        ret = port_is_free(self.job)

        self.assertTrue(ret)

    def test_port_is_free_returns_false_if_port_is_already_bound(self):
        ret = port_is_free(self.job)

        self.assertFalse(ret)
