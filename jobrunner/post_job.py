from contextlib import closing, contextmanager
from logging import getLogger

from taskflow.persistence import backends as persistence_backends
from taskflow.persistence import models as persistence_models

from jobrunner.settings import PERSISTENCE_CONF, LOGBOOK_NAME

log = getLogger(__name__)


@contextmanager
def persistence_backend_connection():
    """
    Get a connection to the persistence backend and yield
    the connection to the context
    :yield obj conn: The persistence backend connection
    """
    persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
    with closing(persist_backend.get_connection()) as conn:
        yield conn


def get_logbook_by_name(logbook_name, conn):
    """
    Get a logbook by name from a persistence backend connection
    :param str logbook_name: The name of the logbook to get
    :param obj conn: A persistence backend connection
    :return obj logbook: The logbook with the specified name
    """
    return next(
        iter([i for i in conn.get_logbooks() if i.name == logbook_name])
    )


def ensure_logbook_exists():
    """
    Ensure the configured logbook exists in the persistence backend
    :return None:
    """
    log.debug(
        "Ensuring logbook {} exists in "
        "persistence backend".format(LOGBOOK_NAME)
    )
    with persistence_backend_connection() as conn:
        conn.upgrade()
        try:
            get_logbook_by_name(LOGBOOK_NAME, conn)
        except StopIteration:
            lb = persistence_models.LogBook(LOGBOOK_NAME)
            conn.save_logbook(lb)


def perform_post():
    """
    Connect to the job board backend and queue the job
    :return None:
    """
    pass


def post_job():
    """
    Post a job to the jobboard
    :return None:
    """
    ensure_logbook_exists()
    perform_post()
