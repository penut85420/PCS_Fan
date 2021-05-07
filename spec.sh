#!/bin/bash

clear

export FOCUS="Hanabi,River,Maple,Doggo,Kaiwing,Kartis"
export IMPORTANT="Khan,Canyon,ShowMaker,Ghost,BeryL"
export IMPORTANT="$IMPORTANT,xiaohu,Wei,Cryin,GALA,ming"
export IMPORTANT="$IMPORTANT,Vulcan,PerkZ,Zven,Blader,Fudge"
export IMPORTANT="$IMPORTANT,Carzzy,Armut,Kaiser"
export IMPORTANT="$IMPORTANT,Steal,Evi,Yutapon,Aria,Ceros,Kazu"
export IMPORTANT="$IMPORTANT,brTT,Luci,Tinowns,Robo,Cariok"

while true; do
    /usr/bin/python3 -m tracking.query.spec \
        --focus $FOCUS --important $IMPORTANT
    sleep 60
done

# export FOCUS="Hanabi,River,Maple,Doggo,Kaiwing,Kartis"
# export IMPORTANT="Khan,ShowMaker,Canyon,Ghost,BeryL,Marlang"
