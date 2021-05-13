#!/bin/bash

export RIOT_API_KEY="$( cat api_key )"
GAME_ID="$( /usr/bin/python3 -m tracking.query.game_id $1 )"
/usr/bin/python3 -m tracking.query.spec_cmd $GAME_ID | clip.exe
echo Spector Command Copied!
/usr/bin/python3 -m tracking.query.match $*
