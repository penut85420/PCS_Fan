#!/bin/bash

# 每五分鐘更新一次選手的積分

clear
while true; do
    /usr/bin/python3 -m tracking.query.opgg
    sleep 300
done
