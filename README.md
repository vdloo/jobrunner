Jobrunner
=========

General purpose job runner that uses [OpenStack TaskFlow](https://wiki.openstack.org/wiki/TaskFlow)

## What is this?

This project is a Python job board to which jobs can be posted and to which job consumers
on multiple machines can be attached. The jobs are TaskFlow flows, Python code that specifies
an execute (forward) and revert (backward) method for each step. This allows you to create very
complex processes where you have guarantees of what the end result will look like on either
success or failure. This program attempts to be an extensible implementation of a generic
TaskFlow non-blocking conductor with commandline tools for managing and visualizing running
processes on a job board. You only have to write the jobs yourself, and those can run on the
job board as a plugin of this project.

## Usage

Clone the project, and check out your self written flows in the `jobrunner/flows` directory.
In the `jobrunner/flows/builtin` directory is an example of what flow definition might look
like. The entry point to post the flow can be registered with the `register_job` decorator.
For documentation about how to write flows, look at [this documentation](https://github.com/vdloo/jobrunner/blob/master/docs/writing_flows_and_registering_jobs.md).

1. Create, activate and install the dependencies into a virtualenv

Change directory to the checkout of this project, then create the virtualenv.

```sh
# Make sure you have python-virtualenv installed
source activate_venv
```

2. Set up a Redis and a MySQL somewhere

All your workers will need to be able to access it.

```python
# Edit jobrunner/settings.py
JOBBOARD_CONF = {
    'board': 'redis',
    'host': '1.2.3.4'
}
PERSISTENCE_CONF = {
    "connection": "mysql://taskflow:taskflow@[{}]"
                  "/taskflow".format('1.2.3.4'),
}
```

3. Run a conductor

A conductor is a process that polls for new unclaimed jobs on the job board. When it
claims a new job it will run that 'flow' in a thread until it has completed or failed.

```
# Run a conductor. You can run multiple conductors on multiple machines.
./bin/jobrunner run
```

4. Post a job

By posting a job to the job board the work described in the job you are posting will
be performed by the conductor that sees and locks the job first. A job consists of
a couple of elements: a function that returns a TaskFlow Flow, arguments and keyword
arguments for that function, and a 'store' which is a dict of variables available
to the Tasks in the flow from the beginning.

```
# List all available jobs
./bin/jobrunner post --help

# Check the example job's help menu
./bin/jobrunner post simple_http_webserver --help
```

Post the sample job. This will run the default Python http web server on the conductor
that claims the posted jobs. This job will run indefinitely but it is a nice showcase
of the persistence feature of TaskFlow. When you kill the web server process it will
restart because of the `Times` retry class on the flow, and when you kill the conductor
running the job it will stop refreshing the lock and another conductor will pick up the
flow at the Atom where it left of (being the execute/revert of the `SimpleHTTPServer`
TaskFlow `Task`.

```
./bin/jobrunner post simple_http_webserver --port 8887
```

5. View the job running on the job board
```
./bin/jobrunner show
```

## Features

Currently this project uses the default non-blocking TaskFlow conductor with the MySQL
persistence backend and the Redis job board backend. This results in a batch processing
system with the following characteristics:

### Persistent and High Availability

This job runner runs OpenStack TaskFlow flows. The TaskFlow tooling, conventions and syntax are
great for processes where a lot of uncertainty (like failing APIs and flaky servers) is involved
and persistence and guarantees are required.

The progress of a flow is stored between each state transition. This means that if any machine
running a flow goes offline, a conductor on another machine will see that the lock on the
running job has become stale and pick up the work where the other machine left of.

This makes it so that if you have multiple machines running the job runner, you can program
processes that run and will continue to run on any available machine as long as there is a
machine running a conductor available.

### Not that much configuration

This project abstracts out the whole job board and job executor part of a project implementing
TaskFlow. Basically every time I was implementing the same thing in different projects while
what I really wanted was just to run TaskFlow flows. This project takes away the overhead of
having to code up a conductor and functions that save flow details and logbooks to a job board.
Just register flows in the `flows/` directory and this application will load them into the job
poster.


## Future

Things I would like to add in the future:

- Consul KV backend instead of Redis or ZooKeeper

This would make it possible to not only run a distributed but a completely decentralized job
board.

- Configurable Persistence and Job board backend

Currently this is hardcoded in the settings for convenience, but this should be configurable.

- Integration with [raptiformica](https://github.com/vdloo/raptiformica)

The whole reason I wrote this program was so that I could have a way to distribute work over
my cluster of random machines (mobile phones, laptops, etc). It would be nice to have something
where I can declaratively describe my cluster network in where it posts flows to run certain
services and processes based on what resources are available, and perhaps request resources
based on the work available (like WOL some PC under my bed, or start some cloud instances) to
catch up with work if the available workers can not keep up with the work waiting in the job
queue. But that probably falls beyond the scope of this repo.
