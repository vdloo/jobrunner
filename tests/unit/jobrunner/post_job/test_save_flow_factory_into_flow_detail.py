from mock import Mock

from jobrunner.post_job import save_flow_factory_into_flow_detail
from jobrunner.settings import PERSISTENCE_CONF
from tests.testcase import TestCase
from to_refactor.flows import fixture_flow_factory


class TestSaveFlowFactoryIntoFlowDetail(TestCase):
    def setUp(self):
        self.flow_detail = Mock()
        self.fetch = self.set_up_patch(
            'jobrunner.post_job.persistence_backends.fetch'
        )
        self.save_factory_details = self.set_up_patch(
            'jobrunner.post_job.engines.save_factory_details'
        )

    def test_save_flow_factory_into_flow_detail_fetches_persist_backend(self):
        save_flow_factory_into_flow_detail(self.flow_detail)

        self.fetch.assert_called_once_with(PERSISTENCE_CONF)

    def test_save_flow_factory_into_flow_detail_saves_factory_details(self):
        save_flow_factory_into_flow_detail(self.flow_detail)

        self.save_factory_details.assert_called_once_with(
            flow_detail=self.flow_detail,
            flow_factory=fixture_flow_factory,
            factory_args=[],
            factory_kwargs={},
            backend=self.fetch.return_value
        )