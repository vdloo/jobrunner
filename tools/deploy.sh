#!/bin/bash
consul members | awk '{print$1}' | tail -n+2 | xargs -I {} rsync -avz `pwd` root@[{}]:/tmp/
