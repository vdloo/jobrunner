#!/bin/bash
DEPLOY_HOSTS=$(consul members | awk 'NR!=1{print$1}')
for deploy_host in $DEPLOY_HOSTS; do
    echo "Now deploying to $(ssh root@$deploy_host hostname)"
    ssh root@$deploy_host pkill -f /tmp/jobrunner/bin/jobrunner_run.py
    ssh root@$deploy_host rm -Rf /tmp/jobrunner
    ssh root@$deploy_host mkdir -p /tmp/jobrunner
    rsync -az `pwd` root@[$deploy_host]:/tmp
    ssh root@$deploy_host 'bash -c "cd /tmp/jobrunner; source activate_venv"'
    ssh root@$deploy_host '/usr/bin/env screen -d -m sh -c "PYTHONPATH=/tmp/jobrunner /tmp/jobrunner/.venv/bin/python /tmp/jobrunner/bin/jobrunner_run.py"'
done
