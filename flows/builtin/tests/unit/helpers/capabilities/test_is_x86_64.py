from mock import Mock

from flows.builtin.helpers.capabilities import is_x86_64, set_cached_is_x86_64
from tests.testcase import TestCase


class TestIsX864(TestCase):
    def setUp(self):
        self.job = Mock()
        self.uname = self.set_up_patch(
            'flows.builtin.helpers.capabilities.uname'
        )
        # Pretending this is a os.uname_result object
        self.uname.return_value = (
            'Linux', 'x86_64_host', '3.19.0-56-generic',
            '#62~14.04.1-Ubuntu SMP Fri Mar 11 11:03:15 UTC 2016',
            'x86_64', 'x86_64'
        )
        # Reset the global memoized result every test method
        set_cached_is_x86_64(None)

    def test_is_x86_64_returns_true_if_x86_64(self):
        ret = is_x86_64(self.job)

        self.assertTrue(ret)

    def test_is_x86_64_returns_false_if_i686(self):
        self.uname.return_value = (
            'Linux', 'i686_host', '4.10.13-1-ARCH',
            '#1 SMP PREEMPT Thu Apr 27 12:35:30 CEST 2017',
            'i686', ''
        )

        ret = is_x86_64(self.job)

        self.assertFalse(ret)

    def test_is_x86_64_returns_false_if_armv7(self):
        self.uname.return_value = (
            'Linux', 'armv7l_host',
            '3.4.0-perf-g1b1963a-02930-g23f7791',
            '#1 SMP PREEMPT Tue Nov 25 11:03:01 2014',
            'armv7l', ''
        )

        ret = is_x86_64(self.job)

        self.assertFalse(ret)

    def test_is_x86_64_caches_result(self):
        is_x86_64(self.job)
        is_x86_64(self.job)

        # Once, not twice. The second time the cached result is used.
        self.uname.assert_called_once_with()
