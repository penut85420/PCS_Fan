#!/bin/bash

clear

# PSG
export FOCUS="Hanabi,River,Maple,Doggo,Kaiwing,Kartis"
# DK
export IMPORTANT="Khan,Canyon,ShowMaker,Ghost,BeryL"
# RNG
export IMPORTANT="$IMPORTANT,xiaohu,Wei,Cryin,GALA,ming"
# C9
export IMPORTANT="$IMPORTANT,Vulcan,PerkZ,Zven,Blaber,Fudge"
# MAD
export IMPORTANT="$IMPORTANT,Carzzy,Armut,Kaiser"
# PGG
export IMPORTANT="$IMPORTANT,Chazz,Pabu,BioPanther,Decoy,Praedyth,DSN"

while true; do
    /usr/bin/python3 -m tracking.query.spec \
        --focus $FOCUS --important $IMPORTANT
    sleep 60
done
