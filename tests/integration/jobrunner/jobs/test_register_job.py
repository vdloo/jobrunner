from json import loads
from os import environ
from os.path import join
from shutil import rmtree
from tempfile import mkdtemp
from subprocess import check_output
from tests.testcase import TestCase


class TestRegisterJob(TestCase):
    def setUp(self):
        unloaded_script = """
from json import dumps
from jobrunner.settings import JOBS
print(dumps(list(JOBS.keys())))
        """
        loaded_script = """
from json import dumps
from jobrunner.plugins import load_all_plugins
from jobrunner.settings import JOBS

load_all_plugins()

print(dumps(list(JOBS.keys())))
        """
        self.script_dir = mkdtemp()
        scripts = {
            'unloaded.py': unloaded_script,
            'loaded.py': loaded_script
        }

        for file_name, content in scripts.items():
            with open(join(self.script_dir, file_name), 'w') as f:
                f.write(content)

    def tearDown(self):
        rmtree(self.script_dir)

    def test_register_job_does_not_register_unloaded_jobs(self):
        ret = loads(check_output(
            ('python', join(self.script_dir, 'unloaded.py')),
            env=environ
        ).decode('utf-8'))

        self.assertCountEqual(ret, list())

    def test_register_job_registers_loaded_jobs(self):
        ret = loads(check_output(
            ('python', join(self.script_dir, 'loaded.py')),
            env=environ
        ).decode('utf-8'))

        expected_jobs = (
            'simple_http_webserver',
        )
        self.assertCountEqual(ret, expected_jobs)
