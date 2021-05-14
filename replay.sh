#!/bin/bash

export RIOT_API_KEY="$( cat api_key )"
export WSL_RP_DIR="/mnt/f/Documents/League of Legends/Replays"
export WIN_GAME_DIR="D:/Garena/32775/Game/League of Legends.exe"
export WIN_RP_DIR="F:/Documents/League of Legends/Replays"

python3 -m tracking.query.replay
