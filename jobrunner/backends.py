from contextlib import contextmanager, closing
from taskflow.jobs import backends as jobboard_backends
from taskflow.persistence import backends as persistence_backends

from jobrunner.settings import PERSISTENCE_CONF, CONDUCTOR_NAME, JOBBOARD_CONF


@contextmanager
def persistence_backend_connection():
    """
    Get a connection to the persistence backend and yield the connection
    to the context
    :yield obj conn: The persistence backend connection
    """
    persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
    with closing(persist_backend.get_connection()) as conn:
        yield conn


@contextmanager
def jobboard_backend_connection():
    """
    Get a connection to the job board backend and yield the connection
    to the context
    :yield obj conn: The job board backend connection
    """
    persistence_backend = persistence_backends.fetch(PERSISTENCE_CONF)
    job_board_backend = jobboard_backends.fetch(
        CONDUCTOR_NAME, JOBBOARD_CONF, persistence=persistence_backend
    )
    job_board_backend.connect()
    with closing(job_board_backend) as conn:
        yield conn
