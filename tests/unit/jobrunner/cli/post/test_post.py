from mock import Mock

from jobrunner.cli.post import post
from tests.testcase import TestCase


class TestPost(TestCase):
    def setUp(self):
        self.fixture_job = Mock()
        self.JOBS = self.set_up_patch(
            'jobrunner.cli.post.JOBS', {
                'fixture_job': self.fixture_job
            }
        )
        self.expected_argv = [
            '/home/vdloo/code/projects/jobrunner/bin/jobrunner_post.py'
        ]
        self.set_up_patch('jobrunner.cli.post.argv', self.expected_argv)
        self.print_post_help = self.set_up_patch(
            'jobrunner.cli.post.print_post_help'
        )
        self.load_all_plugins = self.set_up_patch(
            'jobrunner.cli.post.load_all_plugins'
        )

    def test_post_loads_all_plugins(self):
        post()

        # Need this to find all decorated flow entrypoints
        # and register them in the JOBS dict in the settings
        self.load_all_plugins.assert_called_once_with()

    def test_post_prints_post_help_if_not_enough_arguments(self):
        post()

        self.print_post_help.assert_called_once_with()

    def test_post_prints_post_help_if_help_specified(self):
        self.expected_argv = [
            '/home/vdloo/code/projects/jobrunner/bin/jobrunner_post.py',
            '--help'
        ]
        self.set_up_patch('jobrunner.cli.post.argv', self.expected_argv)

        post()

        self.print_post_help.assert_called_once_with()

    def test_post_does_not_print_help_if_valid_job_specified(self):
        self.expected_argv = [
            '/home/vdloo/code/projects/jobrunner/bin/jobrunner_post.py',
            'fixture_job'
        ]
        self.set_up_patch('jobrunner.cli.post.argv', self.expected_argv)

        self.assertFalse(self.print_post_help.called)

    def test_post_posts_fixture_job_if_specified(self):
        self.expected_argv = [
            '/home/vdloo/code/projects/jobrunner/bin/jobrunner_post.py',
            'fixture_job'
        ]
        self.set_up_patch('jobrunner.cli.post.argv', self.expected_argv)

        post()

        self.fixture_job.assert_called_once_with([])

    def test_post_posts_fixture_job_with_port_if_specified(self):
        self.expected_argv = [
            '/home/vdloo/code/projects/jobrunner/bin/jobrunner_post.py',
            'fixture_job',
            '--port',
            '22'
        ]
        self.set_up_patch('jobrunner.cli.post.argv', self.expected_argv)

        post()

        self.fixture_job.assert_called_once_with(['--port', '22'])

    def test_post_shows_fixture_job_help_menu_if_specified(self):
        self.expected_argv = [
            '/home/vdloo/code/projects/jobrunner/bin/jobrunner_post.py',
            'fixture_job',
            '--help'
        ]
        self.set_up_patch('jobrunner.cli.post.argv', self.expected_argv)

        post()

        self.fixture_job.assert_called_once_with(['--help'])
