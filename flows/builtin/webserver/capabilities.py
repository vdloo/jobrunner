from platform import uname

from jobrunner.plugins import register_capability

cached_is_x86_64 = None


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
def is_x86_64():
    """
    Check if the conductor is an x86_64 host
    :return bool capable: True if host is capable of running jobs with this
    capability as a requirement, False if not
    """
    global cached_is_x86_64
    if cached_is_x86_64 is None:
        set_cached_is_x86_64(uname()[4] == 'x86_64')
    return cached_is_x86_64
