import os
from os.path import dirname, join
from socket import gethostname

from os.path import realpath

from subprocess import check_output

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir))
PROJECT_DIR = join(dirname(dirname(realpath(__file__))))
BACKEND_HOST = check_output(
    "consul members | grep retropie | awk '{print$2}' | awk -F'[][]' '{print $2}'",
    shell=True
).decode('utf-8').strip()
REDIS_HOST = BACKEND_HOST
MYSQL_HOST = BACKEND_HOST
JOBBOARD_CONF = {
    'board': 'redis',
    'host': REDIS_HOST
}
PERSISTENCE_CONF = {
    "connection": "mysql://simulacra@[{}]"
                  "/simulacra".format(MYSQL_HOST),
}
LOGBOOK_NAME = 'jobrunner'
SHOW_POLLERS = 20
JOBS = dict()
CAPABILITIES = dict()

CONDUCTOR_NAME = gethostname()
