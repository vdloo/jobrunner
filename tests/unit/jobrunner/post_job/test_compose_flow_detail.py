from uuid import uuid4

from jobrunner.post_job import compose_flow_detail
from jobrunner.settings import CONDUCTOR_NAME
from tests.testcase import TestCase


class TestComposeFlowDetail(TestCase):
    def setUp(self):
        self.FlowDetail = self.set_up_patch(
            'jobrunner.post_job.persistence_models.FlowDetail'
        )
        self.uuid4 = self.set_up_patch(
            'jobrunner.post_job.uuid4'
        )
        self.mock_uuid = str(uuid4())
        self.uuid4.return_value.__repr__ = lambda _: self.mock_uuid

    def test_compose_flow_detail_instantiates_flow_detail(self):
        compose_flow_detail()

        self.FlowDetail.assert_called_once_with(
            'flow_from_{}'.format(CONDUCTOR_NAME),
            uuid=self.mock_uuid
        )

    def test_compose_flow_detail_adds_empty_store_to_flow_detail_meta(self):
        compose_flow_detail()

        self.FlowDetail.return_value.meta.update.assert_called_once_with({
            'store': dict()
        })

    def test_compose_flow_detail_adds_store_to_flow_detail_meta(self):
        expected_store = {'some_key': 'some_item'}

        compose_flow_detail(expected_store)

        self.FlowDetail.return_value.meta.update.assert_called_once_with({
            'store': expected_store
        })

    def test_compose_flow_detail_returns_composed_flow_detail(self):
        ret = compose_flow_detail()

        self.assertEqual(ret, self.FlowDetail.return_value)
