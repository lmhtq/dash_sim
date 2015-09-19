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
    
    def parse_log(self, logfile) :
        net_speed = []
        fp = open(logfile)
        content = fp.readlines()
        fp.close()
        for line in content :
            fields = line.split(' ')
            net_speed.append(float(fields[4] ) / float(fields[5]) * 1000.0 )
        return net_speed

    def netspeed(self, ind = -1):
        #mu = 100*1000
        #sigma = 1
        #return random.gauss(mu, sigma)
        #pass
        index = [ind]
        def incr():
            index[0] = index[0] + 1
            if index[0] >= len(self.ns):
                index[0] = 0
            return self.ns[index[0]]
        return incr

if __name__ == "__main__":
    logfile = sys.argv[1]
    ns = Throughput(logfile)
    print ns.ns[0:10]

    print ns.get_speed()
    print ns.get_speed()

    nss = ns.netspeed()
    print nss()
    print nss()
