#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl

TIME=600

{ time ffmpeg -i http://video3.earthcam.com/fecnetwork/9974.flv/chunklist_w1220748217.m3u8 -c:v png -t $TIME -f tee -map 0:v " [f=image2]frame%0000d.png|[f=image2pipe]pipe:" 1>/dev/null ; } 2>~/timing.txt

