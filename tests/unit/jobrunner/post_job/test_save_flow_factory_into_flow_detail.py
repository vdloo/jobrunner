from mock import Mock
from taskflow.patterns import linear_flow as lf

from tests.testcase import TestCase
from jobrunner.post_job import save_flow_factory_into_flow_detail
from jobrunner.settings import PERSISTENCE_CONF


def fixture_flow_factory():
    return lf.Flow("fixture_flow")


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
        save_flow_factory_into_flow_detail(self.flow_detail, fixture_flow_factory)

        self.fetch.assert_called_once_with(PERSISTENCE_CONF)

    def test_save_flow_factory_into_flow_detail_saves_factory_details(self):
        save_flow_factory_into_flow_detail(self.flow_detail, fixture_flow_factory)

        self.save_factory_details.assert_called_once_with(
            flow_detail=self.flow_detail,
            flow_factory=fixture_flow_factory,
            factory_args=[],
            factory_kwargs={},
            backend=self.fetch.return_value
        )

    def test_save_flow_factory_uses_specified_factory_args(self):
        expected_args = [True, False, 'blabla']

        save_flow_factory_into_flow_detail(
            self.flow_detail, fixture_flow_factory,
            factory_args=expected_args
        )

        self.save_factory_details.assert_called_once_with(
            flow_detail=self.flow_detail,
            flow_factory=fixture_flow_factory,
            factory_args=expected_args,
            factory_kwargs={},
            backend=self.fetch.return_value
        )

    def test_save_flow_factory_uses_specified_factory_kwargs(self):
        expected_kwargs = {
            'some_param': True,
            'some_other_param': 'blabla'
        }

        save_flow_factory_into_flow_detail(
            self.flow_detail, fixture_flow_factory,
            factory_kwargs=expected_kwargs
        )

        self.save_factory_details.assert_called_once_with(
            flow_detail=self.flow_detail,
            flow_factory=fixture_flow_factory,
            factory_args=[],
            factory_kwargs=expected_kwargs,
            backend=self.fetch.return_value
        )

