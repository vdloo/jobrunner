Scheduling jobs based on capabilities
=====================================

Jobs can be posted with required capabilities. This means that a conductor
won't pick up the job unless the function associated with that capability
evaluates to `True`. The condition is evaluated by the conductor every
time it attempts to claim a job. Therefore it is a good idea to use
caching in the condition or make the check very simple and fast.

## Registering a capability

Just like jobs as described in the [writing flows and registering jobs](https://github.com/vdloo/jobrunner/blob/master/docs/writing_flows_and_registering_jobs.md) documentation, 
the capabilities are registered with a decorator in a `flows/$MODULE/$SUBMODULE/` 
file. Bundled with `jobrunner` are some examples of various capabilities in
`flows/builtin/helpers/capabilities.py`.

Capabilities can be registered by creating a function that returns `True`
or `False` and decorating it with `@register_capability()`. For example:

```python
from platform import uname

@register_capability()
def is_x86_64(_):
    return uname()[4] == 'x86_64'
    return cached_is_x86_64
```

Note the `_` argument in the function. In this case that parameter is
unused. The conductor passes the job that is attempted to be claimed as an
argument. This is so that the capability function can use information
about the job to determine if the host is eligible to run that job. The
advantage of this is that decisions can be made based on dynamic
information. 

For example the builtin `run_webserver` job has a parameter to define the 
port to use. This port is posted to the job board as part of the job
metadata (details) as part of the initial store provided to the flow
context. The dynamic port could then be accessed like this:

```python
@register_capability()
def port_is_free(job):
    flow_details = get_flow_details_by_uuid(job.details['flow_uuid'])
    port_to_check = flow_details.meta['store']['port']
    # And now a decision could be made based on the port. 
    # In the example netstat is used to check if it's free.
```

## Using capabilities

A job can be defined to use a capability by passing a set of registered
capability names to the `post_job` function. In the `run_webserver`
example the capability function `port_is_free` has been registered. That
function can now be referenced to by the string `port_is_free`.

```python
def run_webserver(port=8080):
    post_job(
        simple_http_server_flow_factory,
        store={
            'port': port
        },
        capabilities={'port_is_free'}
    )
```

More than one capability can be passed for each job. The conductor uses
short circuit evaluation. If more than one is passed and any of the
earlier evaluates to `False`, any remaining capability predicates will not
be executed because the conductor already knows it is not eligible to
claim the job. Note that if the order is significant, an `OrderedSet` can be
used. It is recommended to put the least computationally expensive
predicates first so that heavier checks will only be executed if they
really have to.

Note: if a check takes longer than the job board backend lock timeout, the
lock may expire. Keep the predicates fast and use caching if needed. They
will potentially be executed many times in rapid succession by multiple
servers.

