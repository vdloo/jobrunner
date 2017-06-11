from subprocess import CalledProcessError

from jobrunner.utils import check_nonzero_exit
from tests.testcase import TestCase


class TestCheckNonzeroExit(TestCase):
    def setUp(self):
        self.check_call = self.set_up_patch(
            'jobrunner.utils.check_call'
        )
        self.check_call.return_value = (0, 'bla', '')

    def test_check_nonzero_exit_checks_call(self):
        check_nonzero_exit("echo 'bla'")

        self.check_call.assert_called_once_with(
            "echo 'bla'", shell=True
        )

    def test_check_nonzero_exit_returns_true_if_exits_zero(self):
        ret = check_nonzero_exit("echo 'bla'")

        self.assertTrue(ret)

    def test_check_nonzero_exit_returns_false_if_exits_nonzero(self):
        self.check_call.side_effect = CalledProcessError(
            1, '', 'Killed'
        )

        ret = check_nonzero_exit("echo 'bla'")

        self.assertFalse(ret)
