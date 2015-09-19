import dash
import parse_mpd as pm
import os
import sys
import getopt
import dash as dash
import netspeed as netspeed
import threading

mutex = threading.Lock()

def Demo(mpd_path):
    dash = dash.Dash(mpd_path)
    chunk_index = 0
    bitrates = dash.mpd["bitrates"]
    
    # At begin, select the lowest bitrate
    init_bitrate = bitrates[0]
    
    # get all the chunks' size of this bitrate
    # it is a array, and arr[0] is init _init.mp4
    # arr[1] is xxxxx_4s1.m4s
    chunks_size = dash.mpd[init_bitrate]

def algorithm1(dash):
    pass

def Tick(dash):
    mutex.acquire()
    dash.tick()
    mutx.release()

if __name__ == "__main__":
    mpd_path = sys.argv[1]
    dash = dash.Dash(mpd_path)
    threads = []
    t1 = threading.Thread(target=Tick, args=(dash))
    threads.append(t1)
    t2 = threading.Thread(target=Demo, args=(dash))
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
