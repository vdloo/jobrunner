from mock import Mock, ANY

from jobrunner.post_job import perform_post
from jobrunner.settings import CONDUCTOR_NAME
from tests.testcase import TestCase


class TestPerformPost(TestCase):
    def setUp(self):
        self.log = self.set_up_patch(
            'jobrunner.post_job.log'
        )
        self.jobboard_backend_connection = self.set_up_patch(
            'jobrunner.post_job.jobboard_backend_connection'
        )
        self.jobboard_backend_connection.return_value \
            .__exit__ = lambda a, b, c, d: None
        self.j_connection = Mock()
        self.jobboard_backend_connection.return_value \
            .__enter__ = lambda x: self.j_connection
        self.compose_flow_detail = self.set_up_patch(
            'jobrunner.post_job.compose_flow_detail'
        )
        self.save_flow_detail_to_logbook = self.set_up_patch(
            'jobrunner.post_job.save_flow_detail_to_logbook'
        )
        self.save_flow_factory_into_flow_detail = self.set_up_patch(
            'jobrunner.post_job.save_flow_factory_into_flow_detail'
        )
        self.logbook = Mock()

    def test_perform_post_logs_debug_message(self):
        perform_post(self.logbook)

        self.log.debug.assert_called_once_with(ANY)

    def test_perform_post_uses_job_board_backend(self):
        perform_post(self.logbook)

        self.jobboard_backend_connection.assert_called_once_with()

    def test_perform_post_composes_flow_details(self):
        perform_post(self.logbook)

        self.compose_flow_detail.assert_called_once_with()

    def test_perform_post_saves_flow_detail_to_logbook(self):
        perform_post(self.logbook)

        self.save_flow_detail_to_logbook.assert_called_once_with(
            self.compose_flow_detail.return_value,
            self.logbook
        )

    def test_perform_post_saves_flow_factory_into_flow_detail(self):
        perform_post(self.logbook)

        self.save_flow_factory_into_flow_detail.assert_called_once_with(
            self.compose_flow_detail.return_value
        )

    def test_perform_post_posts_job_using_the_job_backend_connection(self):
        perform_post(self.logbook)

        self.j_connection.post.assert_called_once_with(
            'job-from-{}'.format(CONDUCTOR_NAME),
            book=self.logbook,
            details={'flow_uuid': self.compose_flow_detail.return_value.uuid}
        )
