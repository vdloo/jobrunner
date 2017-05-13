from subprocess import check_output

from taskflow import task
from taskflow.patterns import linear_flow as lf


class ExampleTask(task.Task):
    def execute(self, message):
        print("Running blocking simple HTTP server")
        check_output(
            "python -m http.server 8432"
        )

    def revert(self, *args, **kwargs):
        print("Reverting task..")


def fixture_flow_factory():
    f = lf.Flow("fixture_flow")
    f.add(
        ExampleTask(
            "example_task_1"
        )
    )
    return f
