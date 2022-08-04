#!/bin/sh

echo "http://49.232.229.126:7000/NBI/"

# 启动测试服务器在7000端口上
CURRENT_DIR=$(cd $(dirname $0); pwd)
python ${CURRENT_DIR}/../NBIOnline/manage.py runserver 0:7000
