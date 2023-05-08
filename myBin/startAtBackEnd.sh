#!/bin/sh

echo "http://123.120.6.86:7999/NBI/"

CURRENT_DIR=$(cd $(dirname $0); pwd)

date=`date +%Y%m%d`
mkdir -p ../log
sudo touch ../log/log_${date}.out
nohup python3 ${CURRENT_DIR}/../NBIOnline/manage.py runserver 0:7999>../log/log_${date}.out 2>&1 &

echo "Start Django Server at Background"