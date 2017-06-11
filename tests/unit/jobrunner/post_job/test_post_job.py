from taskflow.patterns import linear_flow as lf

from jobrunner.post_job import post_job
from tests.testcase import TestCase


def fixture_flow_factory():
    return lf.Flow("fixture_flow")


class TestPostJob(TestCase):
    def setUp(self):
        self.ensure_logbook_exists = self.set_up_patch(
            'jobrunner.post_job.ensure_logbook_exists'
        )
        self.perform_post = self.set_up_patch(
            'jobrunner.post_job.perform_post'
        )

    def test_post_job_ensures_logbook_exists(self):
        post_job(fixture_flow_factory)

        self.ensure_logbook_exists.assert_called_once_with()

    def test_post_job_performs_post(self):
        post_job(fixture_flow_factory)

        self.perform_post.assert_called_once_with(
            self.ensure_logbook_exists.return_value,
            fixture_flow_factory,
            store=None,
            factory_args=None,
            factory_kwargs=None,
            capabilities=set()
        )

    def test_post_job_performs_post_with_specified_store(self):
        expected_store = {
            'some_key': 'some_value'
        }

        post_job(fixture_flow_factory, store=expected_store)

        self.perform_post.assert_called_once_with(
            self.ensure_logbook_exists.return_value,
            fixture_flow_factory,
            store=expected_store,
            factory_args=None,
            factory_kwargs=None,
            capabilities=set()
        )

    def test_post_job_performs_post_with_specified_factory_args(self):
        expected_args = [True, False, 'blabla']

        post_job(fixture_flow_factory, factory_args=expected_args)

        self.perform_post.assert_called_once_with(
            self.ensure_logbook_exists.return_value,
            fixture_flow_factory,
            store=None,
            factory_args=expected_args,
            factory_kwargs=None,
            capabilities=set()
        )

    def test_post_job_performs_post_with_specified_factory_kwargs(self):
        expected_kwargs = {
            'some_param': True,
            'some_other_param': 'blabla'
        }

        post_job(fixture_flow_factory, factory_kwargs=expected_kwargs)

        self.perform_post.assert_called_once_with(
            self.ensure_logbook_exists.return_value,
            fixture_flow_factory,
            store=None,
            factory_args=None,
            factory_kwargs=expected_kwargs,
            capabilities=set()
        )

    def test_post_job_performs_post_job_with_specified_capabilities(self):
        expected_capabilities = {'is_x86_64', 'is_ubuntu'}

        post_job(fixture_flow_factory, capabilities=expected_capabilities)

        self.perform_post.assert_called_once_with(
            self.ensure_logbook_exists.return_value,
            fixture_flow_factory,
            store=None,
            factory_args=None,
            factory_kwargs=None,
            capabilities=expected_capabilities
        )
