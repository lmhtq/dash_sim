import dash
import parse_mpd as pm
import os
import sys
import getopt
import dash as ds
import netspeed as netspeed

def Init(dash):
    dash.bitrate = dash.mpd["bitrates"][0]
    init_size = dash.mpd[dash.bitrate][0]
    while init_size > 0:
        init_size = init_size - dash.sim_inteval * dash.get_throughput()
        dash.time = dash.time + dash.sim_inteval
    dash.buffer_len = dash.min_buffer_time
    dash.chunk_index = 1
    dash.select(1)

def Demo(mpd_path, log_path):
    dash = ds.Dash(mpd_path, log_path)
    Init(dash)
    while True:
        Tick(dash)

def algorithm1(dash):
	now_T = dash.get_throughput() # must call this function, 
	now_quality = dash.quality    # must be > 0
	now_buffer_len = dash.buffer_len
	next_chunks_size_of_specific_quality = dash.get_chunks_size()
	dash.select(16)

	pass

def Tick(dash):
    dash.tick()
    if dash.check() == True:
        dash.get_throughput()
        return
    algorithm1(dash)

if __name__ == "__main__":
    mpd_path = sys.argv[1]
    log_path = sys.argv[2]
    Demo(mpd_path, log_path)
