#!/bin/sh

# 先查找可能的PID

PIDs=`ps -ef | grep manage.py | grep -v grep | awk '{print $2}'`

# Or find the PID manually
# ps -ef | grep manage.py

# 在杀掉进程就好
for PID in $PIDs
do
    kill -9 $PID
    echo "Kill $PID"
done
echo "All Killed"
