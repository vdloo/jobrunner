from jobrunner.settings import JOBS


def register_job():
    """
    A decorator to register a job for use with `jobrunner run`

    Usage:
        @register_job()
        def your_function():
            pass

    Now a new key 'register_job' will be created in the settings.JOBS dict
    with as value a reference to the function `your_function`. This is used
    by `jobrunner run` to list and post the job.
    :return func wraps: The wrapped function
    """
    def wrap(f):
        JOBS[f.__name__] = f
        return f
    return wrap
