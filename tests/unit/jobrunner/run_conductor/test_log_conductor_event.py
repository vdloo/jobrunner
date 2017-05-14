from mock import Mock, ANY

from jobrunner.run_conductor import log_conductor_event
from tests.testcase import TestCase


class TestLogConductorEvent(TestCase):
    def setUp(self):
        self.event = 'job_abandoned'
        self.details = {
            'job': Mock(),
            'engine': Mock(),
            'conductor': Mock()
        }
        self.log = self.set_up_patch(
            'jobrunner.run_conductor.log'
        )

    def test_log_conductor_event_logs_debug_message(self):
        log_conductor_event(self.event, self.details)

        self.log.debug.assert_called_once_with(ANY)

    def test_log_conductor_does_not_log_info_message(self):
        log_conductor_event(self.event, self.details)

        self.assertFalse(self.log.info.called)

    def test_log_conductor_message_logs_info_message_if_job_consumed(self):
        event = 'job_consumed'

        log_conductor_event(event, self.details)

        self.log.info.assert_called_once_with(ANY)
