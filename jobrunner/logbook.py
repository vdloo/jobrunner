from contextlib import suppress
from logging import getLogger
from multiprocessing.pool import Pool
from os import system
from time import sleep

from jobrunner.backends import persistence_backend_connection, jobboard_backend_connection
from jobrunner.settings import SHOW_POLLERS

log = getLogger(__name__)


def get_atoms_for_flow(flow, persistence_backend):
    """
    Gets all atoms for a flow
    :param obj flow: A TaskFlow flow
    :param obj persistence_backend: A connection to the persistence backend
    :return iter[obj, ..] all_atoms: An iterable of atom objects
    """
    return persistence_backend.get_atoms_for_flow(flow.uuid)


def get_flows_from_logbook(logbook, persistence_backend):
    """
    Gets all flows for a logbook
    :param obj logbook: A TaskFlow logbook
    :param obj persistence_backend: A connection to the persistence backend
    :return iter[obj, ..] all_flows: An iterable of flow objects
    """
    return persistence_backend.get_flows_for_book(logbook.uuid)


def get_logbooks(persistence_backend):
    """
    Gets all logbooks from a persistence backend
    :param obj persistence_backend: A connection to the persistence backend
    :return iter[obj, ..] all_logbooks: An iterable of logbook objects
    """
    return persistence_backend.get_logbooks()


def get_owner(flow_uuid, jobboard_backend):
    """
    Find the owner of a running job
    :param str flow_uuid: UUID of the flow to find the owner of
    :param obj jobboard_backend: Connection to the jobboard backend
    :return str owner: Name of the conductor owning the job
    """
    for job in jobboard_backend.unfiltered_iterjobs():
        cur_uuid = job.details.get('flow_uuid')
        if cur_uuid and cur_uuid == flow_uuid:
            return jobboard_backend.find_owner(job)


def get_flow_details_by_uuid(flow_uuid):
    """
    Retrieve the flow_details for a flow in the persistence
    backend by uuid
    :param str flow_uuid: UUID of the flow to find the flow_details of
    :return obj flow_details: A TaskFlow FlowDetails object.
    Contains the initial store contents and more.
    """
    with persistence_backend_connection() as p:
        return p.get_flow_details(flow_uuid)


def get_all_logbooks():
    """
    Retrieve all logbooks from the persistence backend and
    translate all the relevant data into a dict structure
    :return iter[dict, ..] all_logbooks_as_dict: An iterable of dicts
    representing all logbooks and their contents currently in the
    persistence backend
    """
    with persistence_backend_connection() as p:
        with jobboard_backend_connection() as j:
            return [
                {
                    'name': lb.name,
                    'meta': lb.meta,
                    'flow_details': [
                        {
                            'uuid': f.uuid,
                            'atom_details': [
                                {
                                    'uuid': a.uuid,
                                    'name': a.name,
                                    'state': a.state,
                                } for a in get_atoms_for_flow(f, p)
                            ],
                            'meta': f.meta,
                            'state': f.state,
                            'owner': get_owner(f.uuid, j)
                        } for f in get_flows_from_logbook(lb, p)
                    ]
                } for lb in get_logbooks(p)
            ]


def print_running_from_logbook(logbook):
    """
    Print all running jobs from a logbook
    :param dict logbook: The logbook to print all running jobs for
    :return None:
    """
    system('clear')
    print("{:<20} {:<37} {:<16} {:<26}".format('NAME', 'ID', 'STATE', 'OWNER'))
    for flow_detail in logbook['flow_details']:
        state = flow_detail['state']
        is_running = state == 'RUNNING'
        is_waiting = not state and not flow_detail['atom_details']
        if is_running or is_waiting:
            with suppress(Exception):
                flow_uuid = flow_detail['uuid']
                owner = flow_detail.get('owner', 'UNCLAIMED')
                name = flow_detail['meta']['factory']['name']
                nice_name = name.split('.')[-1].replace('_flow_factory', '')
                print("{:<20} {:<37} {:<16} {:<26}".format(
                    nice_name, flow_uuid, state or "WAITING", owner)
                )
                for atom_detail in flow_detail['atom_details']:
                    if not atom_detail['name'].endswith(
                        '_retry'
                    ) and not atom_detail['name'].endswith(
                        '_INJECTOR'
                    ):
                        print(
                            "  {:<20} {}".format(
                                atom_detail['name'], atom_detail['state']
                            )
                        )


def query_and_print():
    """
    Query and print the jobs on the job board. This function can take a while.
    :return None:
    """
    while True:
        with suppress(Exception):
            all_logbooks_as_dicts = get_all_logbooks()
            if all_logbooks_as_dicts:
                print_running_from_logbook(all_logbooks_as_dicts[0])


def show_logbook():
    """
    Show information about any jobs currently running
    Uses many threads to poll the job board because the latency
    can be high but the processing power required is low
    :return None:
    """
    pool = Pool(processes=SHOW_POLLERS)
    try:
        for _ in range(SHOW_POLLERS):
            pool.apply(query_and_print)
            sleep(0.1)
    except KeyboardInterrupt:
        pool.terminate()
    except Exception:
        pool.terminate()
    finally:
        pool.close()
        pool.join()
