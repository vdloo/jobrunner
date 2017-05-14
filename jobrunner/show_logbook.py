from contextlib import suppress
from logging import getLogger
from multiprocessing.pool import Pool
from os import system
from time import sleep

from jobrunner.backends import persistence_backend_connection
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


def get_all_logbooks():
    """
    Retrieve all logbooks from the persistence backend and
    translate all the relevant data into a dict structure
    :return iter[dict, ..] all_logbooks_as_dict: An iterable of dicts
    representing all logbooks and their contents currently in the
    persistence backend
    """
    with persistence_backend_connection() as conn:
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
                            } for a in get_atoms_for_flow(f, conn)
                        ],
                        'meta': f.meta,
                        'state': f.state,
                    } for f in get_flows_from_logbook(lb, conn)
                ]
            } for lb in get_logbooks(conn)
        ]


def print_running_from_logbook(logbook):
    """
    Print all running jobs from a logbook
    :param dict logbook: The logbook to print all running jobs for
    :return None:
    """
    system('clear')
    print("{:<20} {:<37} {:<16}".format('NAME', 'ID', 'STATE'))
    for flow_detail in logbook['flow_details']:
        state = flow_detail['state']
        is_running = state == 'RUNNING'
        is_waiting = not state and not flow_detail['atom_details']
        if is_running or is_waiting:
            with suppress(Exception):
                flow_uuid = flow_detail['uuid']
                name = flow_detail['meta']['factory']['name']
                nice_name = name.split('.')[-1].replace('_flow_factory', '')
                print("{:<20} {:<37} {:<16}".format(
                    nice_name, flow_uuid, state or "WAITING")
                )
                for atom_detail in flow_detail['atom_details']:
                    if not atom_detail['name'].endswith('_retry'):
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
