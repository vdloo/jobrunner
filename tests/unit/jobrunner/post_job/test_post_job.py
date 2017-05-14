from jobrunner.post_job import post_job
from tests.testcase import TestCase


class TestPostJob(TestCase):
    def setUp(self):
        self.ensure_logbook_exists = self.set_up_patch(
            'jobrunner.post_job.ensure_logbook_exists'
        )
        self.perform_post = self.set_up_patch(
            'jobrunner.post_job.perform_post'
        )

    def test_post_job_ensures_logbook_exists(self):
        post_job()

        self.ensure_logbook_exists.assert_called_once_with()

    def test_post_job_performs_post(self):
        post_job()

        self.perform_post.assert_called_once_with()
