from jobrunner.cli import post
from tests.testcase import TestCase


class TestPost(TestCase):
    def setUp(self):
        self.parse_post_arguments = self.set_up_patch(
            'jobrunner.cli.parse_post_arguments'
        )
        self.post_job = self.set_up_patch(
            'jobrunner.cli.post_job'
        )

    def test_post_parses_post_arguments(self):
        post()

        self.parse_post_arguments.assert_called_once_with()

    def test_post_posts_job(self):
        post()

        self.post_job.assert_called_once_with()
