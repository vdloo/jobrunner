from mock import Mock, call
from taskflow.types.sets import OrderedSet

from jobrunner.iterator import jobboard_iterator
from tests.testcase import TestCase

fake_job_without_capability_requirements = Mock(
    details={'capabilities': set()}
)
fake_job_with_satisfied_capability_requirements = Mock(
    details={'capabilities': {'is_x86_64'}}
)
fake_job_with_unsatisfied_capability_requirements = Mock(
    details={
        # OrderedSet because we test the is_armv7 short circuit. is_ubuntu
        # should never be evaluated in the
        # test_jobboard_iterator_checks_the_capability_of_every_job
        # tescase method below
        'capabilities': OrderedSet(['is_blabla', 'is_armv7', 'is_ubuntu'])
    }
)


def fake_iterjobs(only_unclaimed=False, ensure_fresh=False):
    """
    Fake iterjobs function. This function is normally a method of
    the jobboard connection object.
    :param bool only_unclaimed: Only iterate over the unclaimed jobs.
    Not used in this mock implemtation
    :param bool ensure_fresh: Ensure the jobs that are iterated over are fresh
    Not used in this mock implemtation
    :return iterable[obj, ..] jobs: Iterator that yields eligible jobs
    """
    return iter([
        fake_job_without_capability_requirements,
        fake_job_with_satisfied_capability_requirements,
        fake_job_with_unsatisfied_capability_requirements
    ])


class TestJobboardIterator(TestCase):
    def setUp(self):
        self.has_capability = self.set_up_patch(
            'jobrunner.iterator.has_capability'
        )
        self.has_capability.side_effect = (
            True,  # pretend is_x86_64 evaluates to True
            True,  # pretend is_blabla evaluates to True
            False,  # pretend is_armv7 evaluates to False
            # The is_ubuntu return_value is left out because this should be
            # short-circuited by is_armv7 returning False in the
            # fake_job_with_unsatisfied_capability_requirements
            # evaluation. If it is not short-circuited out the testcases
            # should raise a StopIteration exception.
            # True  # would pretend is_ubuntu evaluates to True,
            # but we don't have to because we never get there.
        )

    def test_jobboard_iterator_checks_the_capability_of_every_job(self):
        ret_func = jobboard_iterator(fake_iterjobs)

        # Return value is lazy. Must consume to trigger
        # side effects. That's what the list() is for
        list(ret_func())

        expected_calls = map(
            call, (
                'is_x86_64',
                'is_blabla',
                'is_armv7',
                # note that 'is_ubuntu' is short-circuited out by all()
                # if any earlier capability evaluated to False, all remaining
                # capabilities for that job will not be checked.
            )
        )

        self.assertCountEqual(
            self.has_capability.mock_calls, expected_calls
        )

    def test_jobboard_iterator_uses_lazy_evaluation(self):
        ret_func = jobboard_iterator(fake_iterjobs)

        ret_func()

        self.assertFalse(self.has_capability.called)

    def test_jobboard_iterator_checks_no_capability_if_no_jobs(self):
        ret_func = jobboard_iterator(
            lambda only_unclaimed, ensure_fresh: iter(list())
        )

        # Return value is lazy. Must consume to trigger
        # side effects. That's what the list() is for
        list(ret_func())

        self.assertFalse(self.has_capability.called)

    def test_jobboard_iterator_returns_jobs_with_satisfied_capabilities(self):
        ret_func = jobboard_iterator(fake_iterjobs)

        expected_jobs = (
            fake_job_without_capability_requirements,
            fake_job_with_satisfied_capability_requirements
        )
        self.assertCountEqual(ret_func(), expected_jobs)
