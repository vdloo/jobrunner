from mock import Mock, ANY
from taskflow.patterns import linear_flow as lf

from jobrunner.post_job import perform_post
from jobrunner.settings import CONDUCTOR_NAME
from tests.testcase import TestCase


def fixture_flow_factory():
    return lf.Flow("fixture_flow")


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
        perform_post(self.logbook, fixture_flow_factory)

        self.log.debug.assert_called_once_with(ANY)

    def test_perform_post_uses_job_board_backend(self):
        perform_post(self.logbook, fixture_flow_factory)

        self.jobboard_backend_connection.assert_called_once_with()

    def test_perform_post_composes_flow_details(self):
        perform_post(self.logbook, fixture_flow_factory)

        expected_store = dict()
        self.compose_flow_detail.assert_called_once_with(
            expected_store
        )

    def test_perform_post_composed_flow_details_with_specified_store(self):
        expected_store = {
            'some_key': 'some_value'
        }

        perform_post(self.logbook, fixture_flow_factory, store=expected_store)

        self.compose_flow_detail.assert_called_once_with(
            expected_store
        )

    def test_perform_post_saves_flow_detail_to_logbook(self):
        perform_post(self.logbook, fixture_flow_factory)

        self.save_flow_detail_to_logbook.assert_called_once_with(
            self.compose_flow_detail.return_value,
            self.logbook
        )

    def test_perform_post_saves_flow_factory_into_flow_detail(self):
        perform_post(self.logbook, fixture_flow_factory)

        self.save_flow_factory_into_flow_detail.assert_called_once_with(
            self.compose_flow_detail.return_value,
            fixture_flow_factory,
            factory_args=None,
            factory_kwargs=None
        )

    def test_perform_post_saves_flow_factory_into_flow_detail_with_args(self):
        expected_args = [True, False, 'blabla']

        perform_post(
            self.logbook, fixture_flow_factory, factory_args=expected_args
        )

        self.save_flow_factory_into_flow_detail.assert_called_once_with(
            self.compose_flow_detail.return_value,
            fixture_flow_factory,
            factory_args=expected_args,
            factory_kwargs=None
        )

    def test_perform_post_saves_flow_factory_into_f_detail_with_kwargs(self):
        expected_kwargs = {
            'some_param': True,
            'some_other_param': 'blabla'
        }

        perform_post(
            self.logbook, fixture_flow_factory, factory_kwargs=expected_kwargs
        )

        self.save_flow_factory_into_flow_detail.assert_called_once_with(
            self.compose_flow_detail.return_value,
            fixture_flow_factory,
            factory_args=None,
            factory_kwargs=expected_kwargs
        )

    def test_perform_post_posts_job_using_the_job_backend_connection(self):
        perform_post(self.logbook, fixture_flow_factory)

        expected_details = {
            'flow_uuid': self.compose_flow_detail.return_value.uuid,
            'capabilities': set()
        }
        self.j_connection.post.assert_called_once_with(
            'job-from-{}'.format(CONDUCTOR_NAME),
            book=self.logbook,
            details=expected_details
        )

    def test_perform_post_posts_job_with_specified_capabilities(self):
        perform_post(
            self.logbook, fixture_flow_factory,
            capabilities={'is_x86_64', 'is_ubuntu'}
        )

        expected_details = {
            'flow_uuid': self.compose_flow_detail.return_value.uuid,
            'capabilities': {'is_x86_64', 'is_ubuntu'}
        }
        self.j_connection.post.assert_called_once_with(
            'job-from-{}'.format(CONDUCTOR_NAME),
            book=self.logbook,
            details=expected_details
        )
