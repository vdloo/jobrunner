from logging import getLogger
from uuid import uuid4
from taskflow import engines
from taskflow.persistence import backends as persistence_backends
from taskflow.persistence import models as persistence_models

from jobrunner.backends import persistence_backend_connection, \
    jobboard_backend_connection
from jobrunner.settings import PERSISTENCE_CONF, LOGBOOK_NAME, CONDUCTOR_NAME

log = getLogger(__name__)


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


def save_flow_detail_to_logbook(flow_detail, logbook):
    """
    Save a flow detail to a logbook
    :param obj flow_detail: A flow detail
    :param obj logbook: A logbook
    :return None:
    """
    logbook.add(flow_detail)
    with persistence_backend_connection() as conn:
        conn.save_logbook(logbook)


def save_flow_factory_into_flow_detail(
    flow_detail, flow_factory, factory_args=None, factory_kwargs=None
):
    """
    Save a flow factory into a flow detail
    :param obj flow_detail: A flow detail
    :param obj flow_factory: A function that returns a flow
    :param list factory_args: The args to pass to the flow factory
    during flow pickup time in the conductor
    :param dict factory_kwargs: The kwargs to pass to the flow factory
    during flow pickup time in the conductor
    :return None:
    """
    persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
    engines.save_factory_details(
        flow_detail=flow_detail,
        flow_factory=flow_factory,
        factory_args=factory_args or list(),
        factory_kwargs=factory_kwargs or dict(),
        backend=persist_backend
    )


def perform_post(
    logbook, flow_factory, store=None, factory_args=None, factory_kwargs=None,
    capabilities=set()

):
    """
    Connect to the job board backend and queue the job
    :param obj logbook: The logbook to post the job to
    :param obj flow_factory: A function that returns a flow
    :param dict store: The store to post with the flow
    :param list factory_args: The args to pass to the flow factory
    during flow pickup time in the conductor
    :param dict factory_kwargs: The kwargs to pass to the flow factory
    during flow pickup time in the conductor
    :param set [str, ..] capabilities: A list of capabilities the the
    conductor should satisfy to view the job as allowed to claim.
    See the register_capability decorator for registering new capabilities
    :return None:
    """
    log.debug("Posting job to the job board")
    with jobboard_backend_connection() as job_backend:
        flow_detail = compose_flow_detail(store or dict())
        save_flow_detail_to_logbook(flow_detail, logbook)
        save_flow_factory_into_flow_detail(
            flow_detail, flow_factory,
            factory_args=factory_args,
            factory_kwargs=factory_kwargs
        )
        job_backend.post(
            "job-from-{}".format(CONDUCTOR_NAME), book=logbook, details={
                # Need this to find the job back in the logbook
                # See _flow_detail_from_job
                # http://pydoc.net/Python/taskflow/0.6.1/
                # taskflow.conductors.base/
                'flow_uuid': flow_detail.uuid,
                'capabilities': capabilities
            }
        )


def compile_flow(
    flow_factory, store=None, factory_args=None, factory_kwargs=None
):
    """
    Load an engine with the specified flow data and compile the flow
    object, returns a loaded engine.
    :param obj flow_factory: A function that returns a flow
    :param dict store: The store to post with the flow
    :param list factory_args: The args to pass to the flow factory
    during flow pickup time in the conductor
    :param dict factory_kwargs: The kwargs to pass to the flow factory
    during flow pickup time in the conductor
    :return obj engine: The loaded engine
    """
    engine = engines.load_from_factory(
        flow_factory, factory_args=factory_args,
        factory_kwargs=factory_kwargs, store=store
    )
    engine.compile()
    engine.prepare()
    engine.validate()
    return engine


def print_hierarchy(engine, format_line=None):
    """
    Print the hierarchy of the flow loaded in the provided engine
    :param obj engine: A loaded taskflow engine
    :param func format_line: A function to format the nodes in the
    engine.compilation.hierarchy lines.
    :return None:
    """
    hierarchy = engine.compilation.hierarchy
    # https://github.com/openstack/taskflow/blob/master/taskflow/engines/action_engine/compiler.py#L364
    for line in hierarchy.pformat(stringify_node=format_line).splitlines():
        print(line)


def draw_hierarchy(
    flow_factory, store=None, factory_args=None, factory_kwargs=None
):
    """
    Compile the flow and print the execution graph
    :param obj flow_factory: A function that returns a flow
    :param dict store: The store to post with the flow
    :param list factory_args: The args to pass to the flow factory
    during flow pickup time in the conductor
    :param dict factory_kwargs: The kwargs to pass to the flow factory
    during flow pickup time in the conductor
    :return None:
    """
    engine = compile_flow(
        flow_factory, store=store,
        factory_args=factory_args, factory_kwargs=factory_kwargs
    )
    print_hierarchy(engine)


def post_job(
    flow_factory, store=None, factory_args=None, factory_kwargs=None,
    capabilities=set(), hierarchy=False
):
    """
    Post a job to the job board
    :param obj flow_factory: A function that returns a flow
    :param dict store: The store to post with the flow
    :param list factory_args: The args to pass to the flow factory
    during flow pickup time in the conductor
    :param dict factory_kwargs: The kwargs to pass to the flow factory
    during flow pickup time in the conductor
    :param set [str, ..] capabilities: A list of capabilities the the
    conductor should satisfy to view the job as allowed to claim.
    See the register_capability decorator for registering new capabilities
    :param hierarchy: Print the execution graph of what the job would
    look like if compiled by the conductor at this moment.
    :return None:
    """
    if hierarchy:
        draw_hierarchy(
            flow_factory,
            store=store,
            factory_args=factory_args,
            factory_kwargs=factory_kwargs
        )
    else:
        logbook = ensure_logbook_exists()
        perform_post(
            logbook, flow_factory,
            store=store,
            factory_args=factory_args,
            factory_kwargs=factory_kwargs,
            capabilities=capabilities
        )
