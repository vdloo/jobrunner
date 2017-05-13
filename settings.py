import os

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir))
JOBBOARD_CONF = {
    'board': 'redis',
    'host': 'fc63:2207:6b22:91e5:5b0b:ef32:4786:c262'
}
PERSISTENCE_CONF = {
    "connection": "mysql://taskflow:taskflow@[fc63:2207:6b22:91e5:5b0b:ef32:4786:c262]/taskflow",
}
cPERSISTENCE_URI = "mysql:///taskflow@taskflow   {}".format(os.path.join(top_dir, 'db.sqlite3'))
LOGBOOK_NAME = 'jobrunner'
CONDUCTOR_NAME = 'conductor'
