#!/bin/bash

clear

while true; do
    /usr/bin/python3 -m tracking.query.players
    echo $( date +"Players Updated: %Y-%m-%d %H:%M:%S" )
    sleep 3600
done
