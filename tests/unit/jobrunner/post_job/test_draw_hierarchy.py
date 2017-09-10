from taskflow.patterns import linear_flow as lf

from jobrunner.post_job import draw_hierarchy
from tests.testcase import TestCase


def fixture_flow_factory():
    return lf.Flow("fixture_flow")


class TestDrawHierarchy(TestCase):
    def setUp(self):
        self.compile_flow = self.set_up_patch(
            'jobrunner.post_job.compile_flow'
        )
        self.print_hierarchy = self.set_up_patch(
            'jobrunner.post_job.print_hierarchy'
        )
        self.keyword_arguments = {
            'store': {'key': 'value'},
            'factory_args': ['some', 'args'],
            'factory_kwargs': {'some': 'kwargs'}
        }

    def test_draw_hierarchy_compiles_flow(self):
        draw_hierarchy(fixture_flow_factory, **self.keyword_arguments)

        self.compile_flow.assert_called_once_with(
            fixture_flow_factory, **self.keyword_arguments
        )

    def test_draw_hierarchy_prints_hierarchy(self):
        draw_hierarchy(fixture_flow_factory, **self.keyword_arguments)

        self.print_hierarchy.assert_called_once_with(
            self.compile_flow.return_value
        )
