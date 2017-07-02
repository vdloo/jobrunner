import os
from os.path import dirname, join
from socket import gethostname

from os.path import realpath

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir))
PROJECT_DIR = join(dirname(dirname(realpath(__file__))))
# todo: get the IP from the ENV or a flag
REDIS_HOST = 'redis.service.consul'
MYSQL_HOST = 'mysql.service.consul'
JOBBOARD_CONF = {
    'board': 'redis',
    'host': REDIS_HOST
}
PERSISTENCE_CONF = {
    "connection": "mysql://taskflow:taskflow@[{}]"
                  "/taskflow".format(MYSQL_HOST),
}
LOGBOOK_NAME = 'jobrunner'
SHOW_POLLERS = 20
JOBS = dict()
CAPABILITIES = dict()

CONDUCTOR_NAME = gethostname()
