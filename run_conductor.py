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

from taskflow.conductors import backends as conductor_backends
from taskflow.exceptions import StorageFailure
from taskflow.jobs import backends as job_backends
from taskflow.persistence import backends as persistence_backends
from settings import JOBBOARD_CONF, CONDUCTOR_NAME, PERSISTENCE_CONF


def print_con_event(event, details):
    print("Event '{}' has been received...".format(event))
    if event == 'job_consumed':
        print('Job completed!')


def run_conductor():
    print("Starting conductor")
    persist_backend = persistence_backends.fetch(PERSISTENCE_CONF)
    with contextlib.closing(persist_backend):
        job_backend = job_backends.fetch(CONDUCTOR_NAME, JOBBOARD_CONF,
                                         persistence=persist_backend)

        job_backend.connect()
        with contextlib.closing(job_backend):
            cond = conductor_backends.fetch('nonblocking', CONDUCTOR_NAME, job_backend,
                                            persistence=persist_backend)
            cond.notifier.register(cond.notifier.ANY, print_con_event)
            try:
                cond.run()
            finally:
                cond.stop()
                cond.wait()


def main():
    run_conductor()


if __name__ == '__main__':
    main()
