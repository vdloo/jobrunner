from contextlib import suppress
from functools import partial
from logging import getLogger

from jobrunner.settings import CAPABILITIES, CONDUCTOR_NAME

log = getLogger(__name__)


def already_owned(jobboard_job=None):
    """
    Check if the job is already owned by this conductor
    :param obj jobboard_job: TaskFlow jobboard job
    :return bool already_owned: True if this conductor already owns the job,
     False if not
    """
    # In case no owner is available yet. Taskflow will attempt to decode
    # even though the value will be None and throw a TypeError :/
    # todo: find a better way to check the owner,
    # catching the TypeError is not nice
    with suppress(TypeError):
        if jobboard_job.board.find_owner(jobboard_job) == CONDUCTOR_NAME:
            log.debug(
                "Already own job {}. Assuming capabilities "
                "satisfied".format(jobboard_job.uuid)
            )
            return True
    return False


def has_capability(capability, jobboard_job=None):
    """
    Check if the local machine has the specified capability
    :param str capability: The capability to evaluate
    :param obj jobboard_job: TaskFlow jobboard job
    :return bool capable: True if it has the capability, False if not
    """
    # If the job is already owned by this conductor need to assume
    # it is capable of executing the job. If we don't and the
    # capability changes (like when a job allocates a port which
    # is a pre-condition to be free for that job) then the iterator
    # will not be able to keep the lock alive because it won't see
    # the job anymore as soon as the capability becomes unavailable.
    if already_owned(jobboard_job):
        return True

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
    capable = CAPABILITIES[capability](jobboard_job)
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
        return all(
            map(
                partial(has_capability, jobboard_job=jobboard_job),
                jobboard_job.details['capabilities']
            )
        )

    def iterate(only_unclaimed=False, ensure_fresh=False):
        return filter(check_all_capabilities, iterjobs(
            only_unclaimed=only_unclaimed,
            ensure_fresh=ensure_fresh
        ))

    return iterate
