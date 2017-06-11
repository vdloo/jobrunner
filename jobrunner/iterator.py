from logging import getLogger

from jobrunner.settings import CAPABILITIES

log = getLogger(__name__)


def has_capability(capability):
    """
    Check if the local machine has the specified capability
    :param str capability: The capability to evaluate
    :return bool capable: True if it has the capability, False if not
    """
    if capability not in CAPABILITIES.keys():
        log.debug(
            "Conductor does not have the capability '{}' check "
            "registered required for this job. Assuming not capable, "
            "skipping job.".format(capability)
        )
        return False
    log.debug(
        "Checking if conductor has capability '{}' "
        "required for this job.".format(capability)
    )
    capable = CAPABILITIES[capability]()
    if capable:
        log.debug(
            "Capability '{}' satisfied. Will attempt "
            "to claim if any other required capabilities "
            "are available as well.".format(capability)
        )
    else:
        log.debug(
            "Capability '{}' NOT satisfied. Skipping job.".format(capability)
        )
    return capable


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
        return all(map(has_capability, jobboard_job.details['capabilities']))

    def iterate(only_unclaimed=False, ensure_fresh=False):
        return filter(check_all_capabilities, iterjobs(
            only_unclaimed=only_unclaimed,
            ensure_fresh=ensure_fresh
        ))

    return iterate
