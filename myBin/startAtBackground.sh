#!/bin/sh

CURRENT_DIR=$(cd $(dirname $0); pwd)
nohup python3 ${CURRENT_DIR}/../NBIOnline/manage.py runserver 0:7000>djo.out 2>&1 &

echo "Start Django Server at Background"