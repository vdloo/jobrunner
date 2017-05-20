import os
from os.path import dirname, join
from socket import gethostname
from subprocess import check_output, CalledProcessError

from os.path import realpath

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir))
PROJECT_DIR = join(dirname(dirname(realpath(__file__))))
# todo: get the IP from the ENV or a flag
HARDCODED_INTERNAL_IP = 'fc63:2207:6b22:91e5:5b0b:ef32:4786:c262'
JOBBOARD_CONF = {
    'board': 'redis',
    'host': HARDCODED_INTERNAL_IP
}
PERSISTENCE_CONF = {
    "connection": "mysql://taskflow:taskflow@[{}]"
                  "/taskflow".format(HARDCODED_INTERNAL_IP),
}
LOGBOOK_NAME = 'jobrunner'
SHOW_POLLERS = 20
JOBS = dict()

CONDUCTOR_NAME = gethostname()
