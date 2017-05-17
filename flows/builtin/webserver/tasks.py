from logging import getLogger
from subprocess import check_call

from taskflow.task import Task

log = getLogger(__name__)


class SimpleHTTPServer(Task):
    def execute(self):
        log.info("Running blocking simple HTTP server")
        check_call([
            'python', '-m', 'http.server', '8432'
        ])