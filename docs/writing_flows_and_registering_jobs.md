Writing flows and registering jobs
==================================

The whole point of this project is to create an easy environment to run
python processes in a distributed and high-available manner. But to do
that we first need to write a flow (a process) that we can run.

## Create a skeleton for your job

The first step is creating a directory to keep your jobs in. I suggest
that you do this in a separate repo and then clone that repo into your
jobrunner checkout at `flows/`. Just like how the `builtin` directory
is module containing (example) flows. This way the flows are loosely
coupled from the conductor and the job executor.

```bash
# cd to your jobrunner checkout
projects/jobrunner$ cd flows/
projects/jobrunner/flows$ ls
builtin  __init__.py

# Create a module
projects/jobrunner/flows$ mkdir myflows
projects/jobrunner/flows$ cd myflows/
projects/jobrunner/flows/myflows$ touch __init__.py

# Init a git repo in this dir if you want
git init  # and then push this somewhere
# so you can later deploy the job board by just
# cloning the jobrunner project and your flows
in the flows directory

# Finally create a directory with a skeleton for your job
projects/jobrunner/flows/myflows$ mkdir myjob
projects/jobrunner/flows/myflows$ cd myjob/
projects/jobrunner/flows/myflows/myjob$ touch __init__.py cli.py factory.py post.py tasks.py

# Your dir structure should now look something like:
projects/jobrunner$ find flows/myflows/
flows/myflows/
flows/myflows/myjob
flows/myflows/myjob/factory.py
flows/myflows/myjob/tasks.py
flows/myflows/myjob/post.py
flows/myflows/myjob/cli.py
flows/myflows/myjob/__init__.py
flows/myflows/__init__.py
```

## Create a TaskFlow Task

A TaskFlow `Task` is a Python object that has an execute and a revert method. The
execute method is executed when the task is being processed. When the execute fails
the revert is run. Also when a Task later in the `Flow` fails, the `Flow` will revert
and the revert method of this Task will also be executed. This is very handy for
when you need to clean up resources after a failed attempt. Imagine that you want
a VPS at AWS, you need to create an EC2 instance and an EBS volume. Then you need
to attach the volume to the instance when they are both ready. But if either the
volume or the instance creation fails, you need to clean them both up.

In your created `tasks.py` file write something like this:

```python
from logging import getLogger
from subprocess import check_call

from taskflow.task import Task

log = getLogger(__name__)

class Task1(Task):
    def execute(self, message):
        log.info(
           "Printing the message from the
           store: {}".format(message)
        )

    def revert(*args, **kwargs):
        # Not implemented, this example has nothing to revert
        # You can completely omit the revert method if you want
        # in that case.
        pass
```

## Creating the Flow factory

A `Flow` factory is a function that returns a TaskFlow `Flow`. A reference to
this function is saved to the job board when a job is posted. This means it is
executed just before the conductor runs the flow. This is important to note
because it means that there are different run times.

We have the moment where we post the flow, the moment where the conductor picks
up the job from the job board and the actual flow execution. The last two are
generally very close together, but they do not run in the same thread. That might
have implications for your code.

It is generally a good idea not to post any state in your flows. By this I mean
that you do not write jobs where you retrieve information about resources you will
be manipulating in the process as part of the posting logic. Because then when the
flow is being executed that resource might have changed. If the flow is executed
quickly after being posted this might not be a problem, but you don't have any
guarantees about who or when is going to execute the work.

So instead of writing logic that implements 'change resource x from y to z' it is
wise to assume that the state could have changed and write logic like 'change resource
x to z if it is not already z'. Who knows, another job changing the resource to z might
have already been executed by a worker after retrieving the state of the resource but
before the posted job was executed.

In `factory.py` write something like:
```python
from taskflow.patterns import linear_flow as lf
from taskflow.retry import Times

from flows.myflows.myjob.tasks import Task1


def my_flow_factory(attempts):
    f = lf.Flow(
        "flow_1", # This will show up in `jobrunner show`
        # This Flow won't fail because we only log a message
        # But it is here to demonstrate the flow arg `attempts`.
        retry=Times(attempts)
    )
    f.add(
        Task1(
            "task_1_task_name"  # This will show up in `jobrunner show`
        )
    )
    return f
```

Here we create a function that returns a Taskflow `Flow` object. A `Flow` contains
tasks and describes the dynamic between compontents. In this case a `Times` retry
class is added to the `Flow`. When a `Task` fails in the `Flow` it will be reverted
and retried the amount of times we specify. Note that it is also possible to add other
flows in a `Flow`. Instead of the `linear_flow` you can also use a `graph_flow`. The
difference is that it will determine the order based on the required store elements
and dependencies of the `Tasks` in the `Flow`. The `linear_flow` is just imperative
from top to bottom.

## Creating the job poster

Next we need a function that posts this flow factory to the job board.

```python
# Edit factory.py
from flows.myflows.myjob.factory import my_flow_factory
from jobrunner.post_job import post_job


def run_my_flow(attempts):
    post_job(
        my_flow_factory,
        store={
            'message': "This is the message from the store"
        },
        factory_args=(attempts,)
    )
```

The function `run_my_flow` saves the newly created job to the job board.
This means a reference to the flow factory function, the arguments for that flow
factory function and the initial items to put in the store to make available to the
`Tasks` in the `Flow`. This logic is evaluated when the job is posted to the job
board. The logic in the flow factory is evaluated when the conductor picks up the job
and 'compiles' the `Flow` (creates the graph of all dependencies and possible forward
and backward steps) for execution. The logic in the `Tasks` is executed when the `Flow`
is executed and said `Task` execute or revert methods are being evaluated.


## Creating the CLI entry point

Finally we need to create a CLI entry point that allows us to post this job from the
command line. By registering this function with the `register_job` decorator it will
show up in the `jobrunner post` help menu and it will be callable by running:

```bash
jobrunner post the_name_of_your_job
```

Edit the `cli.py` file and write something like this:
```python
from argparse import ArgumentParser

from flows.myflows.myjob.post import run_my_flow
from flows.myflows.myjob.post import my_flow_factory
from jobrunner.cli.parse import parse_arguments
from jobrunner.plugins import register_job


def parse_myjob_arguments(args=None):
    parser = ArgumentParser()
    parser.add_argument(
        '--attempts', '-a', type=int, default=10
    )
    return parse_arguments(parser, args=args)


@register_job()
def the_name_of_your_job(args=None):
    args = parse_webserver_arguments(args=args)
    run_my_flow(args.attempts)
```

## Posting the flow

Finally your should be able to see your flow in the `jobrunner post` help menu.
You can access your newly created help menu or any other configured options like
any other normal argument parser:

```bash
jobrunner post the_name_of_your_job --help
```

If you've posted the job, you can check the status with `jobrunner show`.
