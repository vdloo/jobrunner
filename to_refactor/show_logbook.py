import contextlib
from taskflow.persistence import backends as persistence_backends

from settings import PERSISTENCE_CONF


@contextlib.contextmanager
def _get_persistence_backend():
    persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
    with contextlib.closing(persist_backend.get_connection()) as conn:
        yield conn


def get_logbooks():
    with _get_persistence_backend() as conn:
        return conn.get_logbooks()


def get_atoms_for_flow(flow):
    with _get_persistence_backend() as conn:
        return conn.get_atoms_for_flow(flow.uuid)


def get_flows_from_logbook(logbook):
    with _get_persistence_backend() as conn:
        return conn.get_flows_for_book(logbook.uuid)


def get_all_jobs():
    return {
        'logbooks': [
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
                            } for a in get_atoms_for_flow(f)
                        ],
                        'meta': f.meta,
                        'state': f.state,
                    } for f in get_flows_from_logbook(lb)
                ]
            } for lb in get_logbooks()
        ]
    }


def main():
    all_jobs = get_all_jobs()
    flow_details = all_jobs['logbooks'][0]['flow_details']
    for flow_detail in flow_details:
        state = flow_detail['state']
        if state == 'RUNNING':
            flow_uuid = flow_detail['uuid']
            name = flow_detail['meta']['factory']['name']
            nice_name = name .replace('flows.', '').replace('_factory', '')
            print("{}->{} {}".format(nice_name, state, flow_uuid))
            for atom_detail in flow_detail['atom_details']:
                print("  {:<20} {}".format(atom_detail['name'], atom_detail['state']))
            print("")

if __name__ == '__main__':
    main()
