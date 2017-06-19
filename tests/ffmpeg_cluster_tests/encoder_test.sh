#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl

#LINK=http://video3.earthcam.com/fecnetwork/8939.flv/.m3u8
LINK=http://manifest.googlevideo.com/api/manifest/hls_playlist/id/gW9f-pYmLYk.0/itag/95/source/yt_live_broadcast/ratebypass/yes/live/1/cmbypass/yes/goi/160/sgoap/gir%3Dyes%3Bitag%3D140/sgovp/gir%3Dyes%3Bitag%3D136/hls_chunk_host/r2---sn-20gq0x-a54e.googlevideo.com/ei/RhA4Wa_YAYfRuAKpqrboCA/playlist_type/DVR/gcr/us/mm/32/mn/sn-20gq0x-a54e/ms/lv/mv/m/pl/16/dover/6/mt/1496846299/ip/128.210.106.81/ipbits/0/expire/1496868005/sparams/ip,ipbits,expire,id,itag,source,ratebypass,live,cmbypass,goi,sgoap,sgovp,hls_chunk_host,ei,playlist_type,gcr,mm,mn,ms,mv,pl/signature/7442650C13BEE3AC8B81B7B436B66584545C00BB.857D14D4F292261EC974B6E9233116AF528ED7FC/key/dg_yt0/playlist/index.m3u8
PWD=`pwd`
EXT=/CAM2ImageTeam/ffmpeg_cluster_tests
SIN=/single_time

TIME=
i=
FRAMES=30
LENGTH=1280
WIDTH=720
ENC=/encoders


# update and make outfile
OUTFILE=${PWD}${EXT}${SIN}/verbose_single_${TIME}s.txt
#OUTFILE=${PWD}${EXT}${SIN}/single_${TIME}s_${i}.txt
#if [ -f "$OUTFILE" ]; then
#	rm $OUTFILE
#fi
#touch $OUTFILE

# run commands and test them
#{ echo "Single time:-----------------------" ; } 1>>$OUTFILE
#{ echo "time: " $TIME "s, iteration: " ${i} } 1>>$OUTFILE
{ time python ${PWD}${EXT}${ENC}/.py $LINK $TIME $FRAMES $LENGTH $WIDTH 1>/dev/null ; } 2>>$OUTFILE
#{ echo " " ;} 1>>$OUTFILE
#{ echo "Double time:-----------------------" ; } 1>>$OUTFILE
#{ time python ${PWD}${EXT}${ENC}/send_to_pipe.py $LINK $TIME $FRAMES $LENGTH $WIDTH 1>/dev/null ; } 2>>$OUTFILE


