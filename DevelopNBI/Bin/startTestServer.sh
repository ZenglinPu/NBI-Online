#!/bin/sh

echo "http://49.232.229.126:7000/NBI/mainPage/"

# 启动测试服务器在7000端口上
python /home/ubuntu/DevelopNBI/manage.py runserver 0:7000
