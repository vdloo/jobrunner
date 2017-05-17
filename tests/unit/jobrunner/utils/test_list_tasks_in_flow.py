from taskflow.patterns import linear_flow as lf
from taskflow.task import FunctorTask

from jobrunner.utils import list_tasks_in_flow
from tests.testcase import TestCase


def noop():
    pass


class TestListTasksInFlow(TestCase):
    def setUp(self):
        self.flow_1 = lf.Flow("flow1")
        self.flow_2 = lf.Flow("flow2")
        self.flow_2.add(
            FunctorTask(
                name='task1', execute=noop
            )
        )
        self.flow_3 = lf.Flow("flow3")
        self.flow_3.add(
            FunctorTask(
                name='task1', execute=noop
            ),
            FunctorTask(
                name='task2', execute=noop
            )
        )

    def test_list_tasks_in_flow_returns_empty_list_for_empty_flow(self):
        ret = list_tasks_in_flow(self.flow_1)

        self.assertEqual(ret, list())

    def test_list_tasks_in_flow_returns_one_item_if_one_item_in_flow(self):
        ret = list_tasks_in_flow(self.flow_2)

        expected_list = ['task1']
        self.assertEqual(ret, expected_list)

    def test_list_tasks_in_flow_returns_two_items_if_two_items_in_flow(self):
        ret = list_tasks_in_flow(self.flow_3)

        print(list(self.flow_3.iter_nodes()))
        expected_list = ['task1', 'task2']
        self.assertEqual(ret, expected_list)
