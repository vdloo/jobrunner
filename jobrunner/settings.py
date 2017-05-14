import os
from socket import gethostname
from subprocess import check_output, CalledProcessError

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir))
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
try:
    CONDUCTOR_NAME = check_output(
        "ip addr show tun0 | grep inet6 | awk '{print$2}'", shell=True
    ).strip().decode('utf-8')
except CalledProcessError:
    CONDUCTOR_NAME = gethostname()
SHOW_POLLERS = 20
