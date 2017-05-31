#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl

TIME=120
LINK=http://video3.earthcam.com/fecnetwork/8671.flv/chunklist_w2021314869.m3u8 #lion cam
# LINK=http://video3.earthcam.com/fecnetwork/9974.flv/chunklist_w1220748217.m3u8 # new york times square street cam

{ time ffmpeg -i $LINK -c:v png -t $TIME -f tee -map 0:v " [f=image2]frame%0000d.png|[f=image2pipe]pipe:" 1>/dev/null ; } 2>~/timing.txt

