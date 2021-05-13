#!/bin/bash

export RIOT_API_KEY="$( cat api_key )"
/usr/bin/python3 -m tracking.query.match -d $*
