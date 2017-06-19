#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl

TIME=1
LINK=http://trtcanlitv-lh.akamaihd.net/i/TRTWORLD_1@321783/master.m3u8
# LINK=http://video3.earthcam.com/fecnetwork/9974.flv/chunklist_w1220748217.m3u8 # new york times square street cam

{ time ffmpeg -i $LINK -c:v png -t $TIME -f tee -map 0:v " [f=image2]frame%0000d.png|[f=image2pipe]pipe:" 1>/dev/null ; } 2>~/timing.txt

