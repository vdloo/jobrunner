from contextlib import closing, contextmanager
from logging import getLogger
from uuid import uuid4

from taskflow import engines
from taskflow.persistence import backends as persistence_backends
from taskflow.jobs import backends as jobboard_backends
from taskflow.persistence import models as persistence_models

from jobrunner.settings import PERSISTENCE_CONF, LOGBOOK_NAME, CONDUCTOR_NAME, JOBBOARD_CONF
from to_refactor.flows import fixture_flow_factory

log = getLogger(__name__)


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
def jobboard_backend_connection(persistence_backend):
    """
    Get a connection to the job board backend and yield the connection
    to the context
    :param obj persistence_backend: Connection to a persistence backend
    :yield obj conn: The job board backend connection
    """
    job_board_backend = jobboard_backends.fetch(
        CONDUCTOR_NAME, JOBBOARD_CONF, persistence=persistence_backend
    )
    with closing(job_board_backend.connect()) as conn:
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
    :return obj logbook: The retrieved or created logbook
    """
    log.debug(
        "Ensuring logbook {} exists in "
        "persistence backend".format(LOGBOOK_NAME)
    )
    with persistence_backend_connection() as conn:
        conn.upgrade()
        try:
            logbook = get_logbook_by_name(LOGBOOK_NAME, conn)
        except StopIteration:
            logbook = persistence_models.LogBook(LOGBOOK_NAME)
            conn.save_logbook(logbook)
    return logbook


def compose_flow_detail(store=None):
    """
    Compose a flow detail for a logbook
    :param dict store: The store to provide to the flow from the injector
    :return obj flow_detail: The composed flow detail
    """
    flow_detail = persistence_models.FlowDetail(
        "flow_from_{}".format(CONDUCTOR_NAME),
        uuid=str(uuid4())
    )
    flow_detail.meta.update({'store': store or dict()})
    return flow_detail


def save_flow_detail_to_logbook(flow_detail, logbook, job_backend):
    """
    Save a flow detail to a logbook
    :param obj flow_detail: A flow detail
    :param obj logbook: A logbook
    :param obj job_backend: The job board backend
    :return None:
    """
    logbook.add(flow_detail)
    job_backend.save_logbook(logbook)


def save_flow_factory_into_flow_detail(flow_detail, persist_backend):
    """
    Save a flow factory into a flow detail
    :param obj flow_detail: A flow detail
    :param obj persist_backend: The persistence backend
    :return None:
    """
    engines.save_factory_details(
        flow_detail=flow_detail,
        flow_factory=fixture_flow_factory,
        factory_args=[],
        factory_kwargs={},
        backend=persist_backend
    )


def perform_post(logbook):
    """
    Connect to the job board backend and queue the job
    :param obj logbook: The logbook to post the job to
    :return None:
    """
    log.debug("Posting job to the job board")
    with persistence_backend_connection() as persist_backend:
        with jobboard_backend_connection(persist_backend) as job_backend:
            flow_detail = compose_flow_detail()
            save_flow_detail_to_logbook(flow_detail, logbook, job_backend)
            save_flow_factory_into_flow_detail(flow_detail, persist_backend)
            job_backend.post(
                "job-from-{}".format(CONDUCTOR_NAME), book=logbook, details={
                    # Need this to find the job back in the logbook
                    # See _flow_detail_from_job
                    # http://pydoc.net/Python/taskflow/0.6.1/
                    # taskflow.conductors.base/
                    'flow_uuid': flow_detail.uuid
                }
            )


def post_job():
    """
    Post a job to the job board
    :return None:
    """
    logbook = ensure_logbook_exists()
    perform_post(logbook)
