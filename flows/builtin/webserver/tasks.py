from logging import getLogger
from subprocess import check_call

from taskflow.task import Task

log = getLogger(__name__)


class SimpleHTTPServer(Task):
    def execute(self, port):
        """
        RUn a python basic HTTP server in a subshell
        in the current working directory using the
        specified port.
        :param int port: The port to use
        :return None:
        """
        log.info("Running blocking simple HTTP server")
        check_call([
            'python3', '-m', 'http.server', str(port)
        ])
