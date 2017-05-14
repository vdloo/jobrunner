from logging import getLogger
from taskflow.persistence import backends as persistence_backends
from taskflow.conductors import backends as conductor_backends

from jobrunner.backends import jobboard_backend_connection
from jobrunner.settings import PERSISTENCE_CONF, CONDUCTOR_NAME

log = getLogger(__name__)


def log_conductor_event(event, details):
    """
    Log state changes in the conductor
    :param str event: The notified event
    :param dict details: Details about the job, engine and conductor (unused)
    :return None:
    """
    log.debug("Event '{}' has been received...".format(event))
    if event == 'job_consumed':
        log.info('Job consumed!')


def run_until_dead(conductor):
    """
    Run the conductor until something bad happens
    :param obj conductor: The TaskFlow conductor
    :return None:
    """
    try:
        log.debug("Will consume jobs until dead")
        conductor.run()
    finally:
        conductor.stop()
        conductor.wait()


def start_conductor(persistence_backend, job_backend):
    """
    Start the conductor
    :param obj persistence_backend: The persistence backend
    :param obj job_backend: The connected job backend
    :return None:
    """
    log.info("Starting conductor")
    conductor = conductor_backends.fetch(
        'nonblocking', CONDUCTOR_NAME, job_backend,
        persistence=persistence_backend
    )
    conductor.notifier.register(
        conductor.notifier.ANY, log_conductor_event
    )
    run_until_dead(conductor)


def run_conductor():
    """
    Run a conductor that processes jobs from the job board
    Registers a logger to log any TaskFlow state changes
    :return None:
    """
    with jobboard_backend_connection() as job_backend:
        persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
        start_conductor(persist_backend, job_backend)
