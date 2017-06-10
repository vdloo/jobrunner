def has_capability(capability):
    """
    Check if the local machine has the specified capability
    :param str capability: The capability to evaluate
    :return bool capable: True if it has the capability, False if not
    """
    return True


def jobboard_iterator(iterjobs):
    """
    Wrap the iterjobs method of a jobboard backend connection
    in an iterator that filters out jobs not meant for this
    conductor based on the metadata of the job.
    :param func iterjobs: The iterjobs method of a jobboard
    backend connection
    :return iter obj job: Taskflow jobs
    """
    def check_all_capabilities(jobboard_job):
        """
        Check if all the job capabilities are satisfied on the conductor
        :param obj jobboard_job: TaskFlow jobboard job
        :return bool capable: True if it has all capabilities, False if not
        """
        return all(map(has_capability, jobboard_job.details['capability']))

    def iterate(only_unclaimed=False, ensure_fresh=False):
        return filter(check_all_capabilities, iterjobs(
            only_unclaimed=only_unclaimed,
            ensure_fresh=ensure_fresh
        ))

    return iterate
