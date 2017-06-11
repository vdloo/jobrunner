from jobrunner.settings import JOBS, CAPABILITIES

from glob import glob

from jobrunner.settings import PROJECT_DIR


def load_all_plugins():
    """
    Load all registered jobs from the flows directory
    :return None:
    """
    for module in glob(PROJECT_DIR + '/flows/*/*/*.py'):
        plugin = module.split(
            '/flows/'
        )[1].replace('/', '.').replace('.py', '')
        __import__('flows.' + plugin)


def register_job():
    """
    A decorator to register a job for use with `jobrunner run`

    Usage:
        @register_job()
        def your_function():
            pass

    Now a new key 'your_function' will be created in the settings.JOBS dict
    with as value a reference to the function `your_function`. This is used
    by `jobrunner run` to list and `jobrunner post` post the job.
    :return func wraps: The wrapped function
    """
    def wrap(f):
        JOBS[f.__name__] = f
        return f
    return wrap


def register_capability():
    """
    A decorator to register a capability. A capability is a function that is
    evaluated in the conductor to determine whether or not a job can be claimed
    on that machine. If the capability function evaluates False, the conductor
    is not allowed to claim the job. If the capability is not present on the
    conductor, the job is also not allowed to be claimed. Only if the function
    evaluates to True on the conductor a job will be picked up. Capabilities
    are posted as a set of strings as part of the job metadata to the job
    board.

    Usage:
        @register_capability()
        def is_x86_64():
            # Implement the check here
            return True

    Now a new key 'is_x86_64' will be created in the settings.JOBS dict
    with as value a reference to the function `is_x86_64`. This is used
    by `jobrunner run` to let the conductor determine if it is allowed to
    claim that job.

    NOTE: It is best to make capability checking functions short-running
    because they will be evaluated many times. They are evaluated if a job
    has the capability listed in the details every time a conductor attempts
    to claim the job, which is potentially many many times if no eligible
    conductor is available to consume the job or the job is long-running.
    All conductors will attempt to claim the job by polling even though it
    is locked and already running somewhere is, this is so the failover can
    be near instantaneous when the lock is released when the conductor running
    the job dies. Memoization might be beneficial if the capability state
    will not ever change and the computation required to determine if the
    host is capable is heavy.

    # NOTE: if order of execution is important for the capabilities in a job,
    you can post them as an OrderedSet(['is_x86_64, 'is_ubuntu']) for example,
    instead of a normal set {'is_x86_64', 'is_ubuntu'} where order is not
    deterministic. This can be convenient when one of multiple capabilities
    requires more computing power to evaluate, if an earlier capability is
    evaluated to False the ones left will be short-circuited out by all()
    in jobrunner.iterator.py

    :return func wraps: The wrapped function
    """
    def wrap(f):
        CAPABILITIES[f.__name__] = f
        return f
    return wrap
