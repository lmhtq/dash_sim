import os,sys
import string
import getopt
import re

def parse_mpd(filename) :
    mpd = {}
    mpd["bitrates"] = []
    fin = open(filename)
    content = fin.readlines()
    fin.close()
    tmp_bps = ""
    for line in content:
        if "minBufferTime" in line:
            line = line.replace('"', '')
            tags = line.split(' ')
            for tag in tags:
                if "minBufferTime" in tag:
                    minbuffertime = tag.split('=')[1][2:-1]
                    mpd["min_buffer"] = float(minbuffertime)
        if "dashed" in line:
            ind1 = line.find('_')
            ind2 = line.find("_onDemand")
            seglen = int(line[ind1+1:ind2-1])
            mpd["seglen"] = seglen
        if "<Representation" in line :
            line = line.replace('"', '')
            line = line.replace('>', '')
            tags = line.split(' ')
            for tag in tags:
                if "bandwidth" in tag:
                    kv = tag.split('=')
                    mpd["bitrates"].append(int(kv[1]))
                    tmp_bps = int(kv[1])
                    mpd[tmp_bps] = []
        if "BaseURL" in line:
            stt = line.find('>')
            end = line.find('/')
            dir = line[stt+1:end]
            dirname = filename.split('/')
            dirname[-1] = dir
            dirname = '/'.join(dirname) + '/'
            mpd[tmp_bps] = fsize(dirname)
    return mpd

def fsize(dirname) :
    files = os.listdir(dirname)
    fp = ""
    finit = ""
    for f in files:
        if "_init" in f:
            ind = f.find('_init')
            fp = f[0:ind]
            finit = f
            break
    farray = []
    farray.append(os.path.getsize(dirname + finit))
    i = 1
    while (True):
        fn = dirname + fp + str(i) + ".m4s"
        if os.path.exists(fn):
            farray.append(os.path.getsize(fn))
        else:
            break
        i = i + 1
    #print farray
    return farray

if __name__ == "__main__" :
    
    for arg in sys.argv:
        print arg
    mpd = parse_mpd(sys.argv[1])
    for k in mpd:
        print k
    print mpd["bitrates"]
    print mpd["min_buffer"]
    print mpd["seglen"]
    bitrates = mpd["bitrates"]
    print mpd[bitrates[0]]
    print mpd[bitrates[1]]
