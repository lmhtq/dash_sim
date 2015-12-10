import dash
import parse_mpd as pm
import os
import sys
import getopt
import dash as ds
import netspeed as netspeed
import math

def set_fix_chunksize(dash):
    bits = dash.mpd["bitrates"]
    for bps in bits:
        bps_str = (bps)
        for i in range(0,len(dash.mpd[bps_str])):
            dash.mpd[bps_str][i] = bps * dash.segment_len
        #print dash.mpd[bps_str]

def Init(dash):
    #set_fix_chunksize(dash)
    dash.bitrate = dash.mpd["bitrates"][0]
    init_size = dash.mpd[dash.bitrate][0]
    while init_size > 0:
        init_size = init_size - dash.sim_inteval * dash.get_throughput()
        dash.time = dash.time + dash.sim_inteval
    dash.buffer_len = dash.segment_len
    dash.chunk_index = 1
    dash.select(1)

def Demo(mpd_path, log_path):
    dash = ds.Dash(mpd_path, log_path)
    Init(dash)
    while True:
        Tick(dash)

def BBA(dash):
    r = 5.0
    cu = 20.0
    T = dash.get_throughput()
    quality = dash.quality
    buffer_len = dash.buffer_len
    new_quality = quality
    max_quality = len(dash.mpd["bitrates"])
    
    quality_plus = quality
    quality_minus = quality
    if quality > max_quality:
        quality_plus = max_quality
    else:
        quality_plus = quality + 1

    if quality <= 1 :
        quality_minus = 1
    else:
        quality_minus = quality - 1

    if buffer_len <= r :
        new_quality = 1
    elif buffer_len >= (r + cu) :
        new_quality = max_quality
    
    tmp = 1 + (buffer_len - r) * (max_quality - 1) / cu
    if tmp >= quality_plus :
        new_quality = math.floor(tmp)
    elif tmp <= quality_minus:
        new_quality = math.ceil(tmp)
    else:
        new_quality = quality

    dash.select(new_quality)
	
def algorithm1(dash):
    now_T = dash.get_throughput() # must call this function, 
    now_quality = dash.quality    # must be > 0
    now_buffer_len = dash.buffer_len
    next_chunks_size_of_specific_quality = dash.get_chunks_size()
    print next_chunks_size_of_specific_quality
    dash.select(16)

def test(dash):
    T = dash.get_throughput()
    max_quality = len(dash.mpd["bitrates"])
    buffer_len = dash.buffer_len

    bitrate = dash.bitrate
    quality = dash.quality
    new_quality = quality

    k = T / dash.segment_len
    tmp_rate = k * buffer_len
    if tmp_rate > bitrate:
        while tmp_rate > dash.quality_to_bitrate(new_quality):
            if new_quality >= max_quality:
                break
            else:
                new_quality = new_quality + 1
        new_quality = new_quality - 1

    elif tmp_rate < bitrate:
        while tmp_rate < dash.quality_to_bitrate(new_quality):
            if new_quality <= 1:
                new_quality = 1
                break
            else:
                new_quality = new_quality - 1

    print "buffer:" + str(buffer_len) + "\tquality:" + str(new_quality)  
    dash.select(new_quality)

def Tick(dash):
    dash.tick()
    if dash.check() == True:
        dash.get_throughput()
        return
    #algorithm1(dash)
    #test(dash)
    BBA(dash)

if __name__ == "__main__":
    mpd_path = sys.argv[1]
    log_path = sys.argv[2]
    Demo(mpd_path, log_path)

