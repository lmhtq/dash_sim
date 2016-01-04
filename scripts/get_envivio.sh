#!/bin/bash

Name="Envivio"

echo "Make a directory"
cd ~/disk/B/test_video
mkdir $Name
cd $Name
wget http://dash.edgesuite.net/envivio/dashpr/clear/Manifest.mpd

video_id=1
while (($video_id<=5));
do 
mkdir video$video_id
echo "Downloading video$video_id"
cd video$video_id
for video_seq in `seq 0 1 64`;
do
wget http://dash.edgesuite.net/envivio/dashpr/clear/video$video_id/$video_seq.m4s
done #for
cd ..
done #while




