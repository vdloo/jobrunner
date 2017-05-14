from subprocess import check_call

from taskflow import task
from taskflow.patterns import linear_flow as lf
from taskflow.retry import Times


class ExampleTask(task.Task):
    def execute(self, message):
        print("Running blocking simple HTTP server")
        check_call(
            "python -m http.server 8432", shell=True
        )

    def revert(self, *args, **kwargs):
        pass


def fixture_flow_factory():
    f = lf.Flow("fixture_flow", retry=Times(10))
    f.add(
        ExampleTask(
            "example_task_1"
        )
    )
    return f
