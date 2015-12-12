import os
import sys
import random
import math
import string

class Throughput():
    def __init__(self, logfile):
        self.ns = self.parse_log(logfile)
        self.netspeed()
        self.get_speed = self.netspeed()
        self.netspeed_idx = 0
    
    def parse_log(self, logfile) :
        net_speed = []
        fp = open(logfile)
        content = fp.readlines()
        for line in content :
            fields = line.split(' ')
            for i in range(0, int(fields[5])):
                net_speed.append(float(fields[4] ) / float(fields[5]) * 1000.0 )
        return net_speed

    def netspeed(self, ind = -1, interval = 1000):
        #mu = 100*1000
        #sigma = 1
        #return random.gauss(mu, sigma)
        #pass
        index = [ind]
        def incr():
            index[0] = index[0] + interval
            if index[0] >= len(self.ns):
                index[0] = 0
            return self.ns[index[0]]
        return incr
    
    def netspeed_idx_val(self, interval = 500):
        idx = (self.netspeed_idx + len(self.ns) ) % len(self.ns)
        self.netspeed_idx = self.netspeed_idx + interval
        return self.ns[idx]

if __name__ == "__main__":
    logfile = sys.argv[1]
    ns = Throughput(logfile)
    print ns.ns[0:10]

    print ns.get_speed()
    print ns.get_speed()

    nss = ns.netspeed(-1, 500)
    print nss()
    print nss()
    print nss()

    print "netspeed_idx_val"
    print ns.netspeed_idx_val()
    print ns.netspeed_idx_val()
    print ns.netspeed_idx_val()
    print ns.netspeed_idx_val()
