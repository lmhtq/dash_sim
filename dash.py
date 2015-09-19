import os
import sys
import string
import time
import parse_mpd as pm

class Dash:
    def __init__(self, mpd_dir):
        self.fp = open("log" + time.ctime(), "w")
        self.buffler_len = 0
        self.mpd = pm.parse_mpd(mpd_dir)
        self.buffer_empty_count = 0
        self.switch_count = 0
        self.time = 0
        self.isempty = 0
    def __del__(self):
        self.fp.close()
    def tick():
        self.time = self.time + 0.1
        self.check()
    def log(msg):
        self.fp.writeline(str(self.time) + ' : ' + msg)
    def check():




