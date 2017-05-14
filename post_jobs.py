# -*- coding: utf-8 -*-
# adapted from http://docs.openstack.org/developer/taskflow/examples.html

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import contextlib
import sys

from oslo_utils import uuidutils
from taskflow import engines
from taskflow.jobs import backends as job_backends
from taskflow.persistence import backends as persistence_backends
from taskflow.persistence import models

from flows import fixture_flow_factory
from settings import top_dir, JOBBOARD_CONF, LOGBOOK_NAME, CONDUCTOR_NAME, PERSISTENCE_CONF

sys.path.insert(0, top_dir)


def get_logbook_by_name(logbook_name, conn):
    return next(iter([i for i in conn.get_logbooks() if i.name == logbook_name]))


def run_poster():
        persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
        job_backend = job_backends.fetch(CONDUCTOR_NAME, JOBBOARD_CONF,
                                         persistence=persist_backend)
        job_backend.connect()
        # Create information in the persistence backend about the
        # unit of work we want to complete and the factory that
        # can be called to create the tasks that the work unit needs
        # to be done.
        with contextlib.closing(persist_backend.get_connection()) as conn:
            lb = get_logbook_by_name(LOGBOOK_NAME, conn)
            fd = models.FlowDetail("flow-from-{}".format(CONDUCTOR_NAME),
                                   uuidutils.generate_uuid())
            fd.meta.update({
                'store': {
                    'message': 'Injector message'
                }
            })
            lb.add(fd)
            conn.save_logbook(lb)

            engines.save_factory_details(
                flow_detail=fd,
                flow_factory=fixture_flow_factory,
                factory_args=[],
                factory_kwargs={},
                backend=persist_backend
            )
            # Post the job to the backend
            job = job_backend.post(
                "job-from-{}".format(CONDUCTOR_NAME), book=lb, details={
                        # Need this to find the job back in the logbook
                        # See _flow_detail_from_job
                        # http://pydoc.net/Python/taskflow/0.6.1/taskflow.conductors.base/
                        'flow_uuid': fd.uuid
                    }
            )
            print("Posted: {}".format(job))


def create_logbook():
    persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
    with contextlib.closing(persist_backend.get_connection()) as conn:
        conn.upgrade()
        try:
            get_logbook_by_name(LOGBOOK_NAME, conn)
        except StopIteration:
            lb = models.LogBook(LOGBOOK_NAME)
            conn.save_logbook(lb)


def main():
    create_logbook()
    run_poster()


if __name__ == '__main__':
    main()
