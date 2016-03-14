import os
import sys
import string
import time
import parse_mpd as pm
import netspeed as netspeed
from collections import deque
import math

class Dash:
    def __init__(self, mpd_dir, log_dir):
        self.fp = open("log_" + time.ctime(), "w")
        self.buffer_len = 0
        self.mpd = pm.parse_mpd(mpd_dir)
        self.buffer_empty_count = 0
        self.buffer_max = 30
        self.switch_count = 0
        self.time = 0
        self.isempty = 0
        self.last_isempty = 0
        self.isdownloading = 0
        self.chunk_downloaded = 0#the one downloading
        self.chunk_size = 0
        self.last_bitrate = 0
        self.bitrate = 0
        self.quality = 1
        self.netspeed = 0
        self.last_netspeed = 0
        self.min_buffer_time = self.mpd["min_buffer"]
        self.segment_len = self.mpd["seglen"]
        self.chunk_index = 0
        self.sim_interval = 0.01 #unit sec
        self.finished = 0
        self.throughput = netspeed.Throughput(log_dir)
        self.fluctuation = 0
        #for ELASTIC
        self.elastic_dT = 0 # the spent time of this segment
        self.elastic_S = 0  # last segment's size
        self.elastic_d = 0  # 1: playing , 0:pause or elastic_q = 0
        self.elastic_q = self.buffer_len  # equal to self.buffer_len
        self.elastic_r = 0  # harmonic filter mean of last (elastic_S/elastic_dT)
        self.elastic_qI = 0
        self.elastic_qT = 16
        self.elastic_T = self.time
        self.elastic_deque = deque(maxlen = 5)

    def __del__(self):
        self.log("Finished!")
        self.log("Max buffer: " + str(self.buffer_max))
        self.log("Switch count: " + str(self.switch_count))
        self.log("Rebuffer count: " + str(self.buffer_empty_count))
        self.fp.close()
    
    def tick(self):
        if self.buffer_len + self.segment_len >= self.buffer_max:
            self.time = self.time + self.sim_interval
            self.buffer_len = self.buffer_len - self.sim_interval
            self.last_isempty = self.isempty
            return

        if self.can_download == 1:
            self.chunk_downloaded = self.chunk_downloaded + self.sim_interval * self.last_netspeed
            #print self.chunk_downloaded, self.chunk_size
            if self.chunk_downloaded >= self.chunk_size:
                self.elastic_S = self.chunk_size
                self.isdownloading = 0
                self.log(str(self.chunk_index) + " Downloaded!")
                self.chunk_index = self.chunk_index + 1
                self.chunk_downloaded = 0
                self.buffer_len = self.buffer_len + self.segment_len
                self.log("Buffer Level: " + str(self.buffer_len))
                self.can_download = 0
            else:
                #pass
                self.isdownloading = 1

        tmp_bps = self.mpd["bitrates"][0]
        chunk_num = len(self.mpd[tmp_bps])
        #print chunk_num
        if self.chunk_index >= chunk_num - 1:
            self.finished = 1
        else:
            self.finished = 0

        #update basic variables
        self.time = self.time + self.sim_interval
        self.buffer_len = self.buffer_len - self.sim_interval
        self.last_isempty = self.isempty
        
        if self.buffer_len <= 0:
            self.buffer_len = 0
            self.log("Buffer Dry Out!")
            self.isempty = 1
        else:
            self.isempty = 0

        self.log("Buffer Level: " + str(self.buffer_len))

        if self.last_isempty == 0 and self.isempty == 1:
            self.buffer_empty_count = self.buffer_empty_count + 1
        #print self.isdownloading, self.can_download
        #time.sleep(0.5)
   
    def log(self, msg):
        info = str(self.time) + ' : ' + msg + '\n'
        #print info
        self.fp.write(info)
    
    def check(self):
        if self.finished == 1:
            self.log("Finished!")
            exit()
        if self.isdownloading == 1:
            return True
        elif self.isdownloading == 0:
            return False

    #this select's rate is quality, it is a index instead of bps
    def select(self, rate):
        self.can_download = 1
        rate = int(rate)
        if rate < 1:
            rate = 1
        if rate >= len(self.mpd["bitrates"]):
            rate = len(self.mpd["bitrates"])
        
        quality = rate
        self.quality = quality
        
        if rate < 100:
            rate = self.mpd["bitrates"][rate - 1]
        
        self.last_bitrate = self.bitrate
        self.bitrate = rate
        self.chunk_size = self.mpd[rate][self.chunk_index]
        self.log("Begin Download: " + str(self.chunk_index) + ", bitrate: " + str(self.bitrate) + " quality:" + str(self.quality) + ", chunk size: " + str(self.chunk_size))
        if (self.last_bitrate != self.bitrate):
            self.switch_count = self.switch_count + 1
            self.log(str(self.chunk_index) + "Rate switched!")
        #print rate, self.chunk_index,len(self.mpd[rate])
        self.isdownloading = 1        

    def get_throughput(self):
        self.last_netspeed = self.netspeed
        interval = self.sim_interval
        self.netspeed = self.throughput.netspeed_idx_val(int(interval * 1000))
        return self.netspeed

    def get_chunks_size(self):
        sizes = []
        for v in self.mpd["bitrates"]:
            sizes.append( self.mpd[v][self.chunk_index] )
        return sizes

    def get_chunk_size(self):
        sizes = self.mpd[self.bitrate]
        return sizes[self.chunk_index]

    def quality_to_bitrate(self, quality):
        bitrates = self.mpd["bitrates"]
        if quality < 1:
            quality = 1;
        if quality >= len(bitrates):
            quality = len(bitrates)
        return bitrates[quality - 1]

    #this select's rate is bps(the named bps, instead of calced one)
    def select_by_rate(self, rate):
        quality = 0
        self.can_download = 1
        rate = int(rate)
        self.last_bitrate = self.bitrate
        self.bitrate = rate
        
        while quality < len(self.mpd["bitrates"]):
            if rate == self.mpd["bitrates"][quality]:
                break
            quality = quality + 1
        quality = quality + 1
        self.quality = quality
        self.chunk_size = self.mpd[rate][self.chunk_index]

        self.log("Begin Download: " + str(self.chunk_index) + ", bitrate: " + str(self.bitrate) + " quality:" + str(self.quality) + ", chunk size: " + str(self.chunk_size))
        if (self.last_bitrate != self.bitrate):
            self.switch_count = self.switch_count + 1
            self.log(str(self.chunk_index) + "Rate switched!")
        #print rate, self.chunk_index,len( self.mpd[rate] )
        self.isdownloading = 1        



