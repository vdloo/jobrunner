from taskflow.patterns import linear_flow as lf

from jobrunner.post_job import compile_flow
from tests.testcase import TestCase


def fixture_flow_factory():
    return lf.Flow("fixture_flow")


class TestCompileFlow(TestCase):
    def setUp(self):
        self.load_from_factory = self.set_up_patch(
            'jobrunner.post_job.engines.load_from_factory'
        )
        self.keyword_arguments = {
            'store': {'key': 'value'},
            'factory_args': ['some', 'args'],
            'factory_kwargs': {'some': 'kwargs'}
        }

    def test_compile_flow_loads_engine(self):
        compile_flow(fixture_flow_factory, **self.keyword_arguments)

        self.load_from_factory.assert_called_once_with(
            fixture_flow_factory, **self.keyword_arguments
        )

    def test_compile_flow_compiles_loaded_engine(self):
        compile_flow(fixture_flow_factory, **self.keyword_arguments)

        self.load_from_factory.return_value.compile.assert_called_once_with()

    def test_compile_flow_prepares_loaded_engine(self):
        compile_flow(fixture_flow_factory, **self.keyword_arguments)

        self.load_from_factory.return_value.prepare.assert_called_once_with()

    def test_compile_flow_validates_loaded_engine(self):
        compile_flow(fixture_flow_factory, **self.keyword_arguments)

        self.load_from_factory.return_value.validate.assert_called_once_with()

    def test_compile_flow_returns_loaded_engine(self):
        ret = compile_flow(fixture_flow_factory, **self.keyword_arguments)

        self.assertEqual(ret, self.load_from_factory.return_value)
