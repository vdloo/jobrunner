from time import time
from platform import uname

from jobrunner.plugins import register_capability
from jobrunner.show_logbook import get_flow_details_by_uuid
from jobrunner.utils import check_nonzero_exit

cached_is_x86_64 = None
cached_port_is_free = None
cached_port_is_free_timestamp = None


def set_cached_is_x86_64(capable):
    """
    Set the memoized is_x86_64 result
    Function so the module level global can be overwritten
    from other modules. The test case uses this to prevent
    leaking the state across test methods.
    :param bool capable: True if capable, False if not
    :return None:
    """
    global cached_is_x86_64
    cached_is_x86_64 = capable


@register_capability()
def is_x86_64(_):
    """
    Check if the conductor is an x86_64 host
    :param obj _: The jobboard job. Unused in the capability
    :return bool capable: True if host is capable of running jobs with this
    capability as a requirement, False if not
    """
    global cached_is_x86_64
    if cached_is_x86_64 is None:
        set_cached_is_x86_64(uname()[4] == 'x86_64')
    return cached_is_x86_64


def set_cached_port_is_free(capable):
    """
    Set the memoized port_is_free result
    Function so the module level global can be overwritten
    from other modules. The test case uses this to prevent
    leaking the state across test methods.
    :param bool capable: True if capable, False if not
    :return None:
    """
    global cached_port_is_free
    cached_port_is_free = capable


def reset_cached_port_is_free_timestamp():
    """
    Reset the memoized port_is_free timestamp to None
    Function so the module level global can be overwritten
    from other modules. The test case uses this to prevent
    leaking the state across test methods.
    :return None:
    """
    global cached_port_is_free_timestamp
    cached_port_is_free_timestamp = None


@register_capability()
def port_is_free(job):
    """
    Check if the specified port is free on the host
    running this conductor.
    :param obj job: TaskFlow jobboard job
    :return bool capable: True if host is capable of running jobs with this
    capability as a requirement, False if not
    """
    global cached_port_is_free
    global cached_port_is_free_timestamp
    flow_details = get_flow_details_by_uuid(job.details['flow_uuid'])
    port_to_check = flow_details.meta['store']['port']

    check_port_free_command = "netstat -tuna | grep -q {:d}".format(port_to_check)

    should_recheck = cached_port_is_free_timestamp is None or time(
    ) - cached_port_is_free_timestamp > 10
    if cached_port_is_free is None or should_recheck:
        set_cached_port_is_free(
            not check_nonzero_exit(check_port_free_command)
        )
        cached_port_is_free_timestamp = time()

    # NOTE: There is a race condition here. If the port becomes unavailable
    # after the check but before the flow allocates the port, the flow will
    # crash. This should be fine though since all jobs should ideally be
    # re-posted if failed and still needed.
    return cached_port_is_free

