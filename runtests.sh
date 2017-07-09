#!/usr/bin/env bash
set -e

while getopts "1i" opt; do
    case $opt in
        1) RUN_ONCE=1;;
        i) INTEGRATION=1;;
    esac
done

[ -z $INTEGRATION ] && TEST_SUITE="unit" || TEST_SUITE="integration"

shift "$((OPTIND-1))"

if [ -e "/proc/cpuinfo" ]; then
    numprocs=$(grep processor /proc/cpuinfo  | wc -l | xargs)
elif [ "x$(uname)" = "xDarwin" ]; then
    numprocs=$(sysctl -n hw.ncpu)
else
    numprocs=1
fi

# Don't write .pyc files
export PYTHONDONTWRITEBYTECODE=1  
# Remove existing .pyc files
find . -type f -name *.pyc -delete

test_script="
    echo 'Running jobrunner $TEST_SUITE tests';
    nosetests --processes=$numprocs tests/$TEST_SUITE $(find flows/*/ -type d -name $TEST_SUITE);
    echo 'Checking PEP8';
    autopep8 -r --diff jobrunner;
"

if [ -z $RUN_ONCE ]; then
    LC_NUMERIC="en_US.UTF-8" watch -c -- "$test_script"
else
    sh -c "$test_script"
fi
