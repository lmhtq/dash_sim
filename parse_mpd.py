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
        if "DASH-MPD.xsd" in line:#dash.edgesuite.net, may be need to find a more identidied label
            return parse_mpd_edgesuite(filename)
        else:#http://www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014
            pass    
	if "minBufferTime" in line:
            line = line.replace('"', '')
            tags = line.split(' ')
            for tag in tags:
                if "minBufferTime" in tag:
                    minbuffertime = tag.split('=')[1][2:-1]
                    mpd["min_buffer"] = float(minbuffertime)
        if "dashed" in line:
            line = filename
            ind1 = line.find('_')
            ind2 = line.find("_onDemand")
            ind1 = line.find('_', ind1 + 1, ind2)
            #print (line[ind1:ind2])
            #print line[ind2], line[ind2-1]
            #print ind1+1, ind2
            if line[ind2-1] == "s":
                seglen = int(line[ind1+1:ind2-1])
            else:
                if ind1+1 == ind2 - 1:
                    seglen = int(line[ind1+1])
                else:
                    seglen = int(line[ind1+1, ind2])
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
    mpd["bitrates"].sort()
    return mpd

def parse_mpd_edgesuite(filename) :
    mpd = {}
    mpd["bitrates"] = []
    fin = open(filename)
    content = fin.readlines()
    fin.close()
    tmp_bps = ""
    for line in content:
        mpd["seglen"] = 4
	if "minBufferTime" in line:
            line2 = line.replace('"', '')
            tags = line2.split(' ')
            for tag in tags:
                if "minBufferTime" in tag:
                    minbuffertime = tag.split('=')[1][2:-1]
                    mpd["min_buffer"] = float(minbuffertime)
        if "<Representation" in line :
            if "audio" in line:
                continue
            line2 = line.replace('"', '')
            line2 = line2.replace('>', '')
            tags = line2.split(' ')
            for tag in tags:
                if "bandwidth" in tag:
                    kv = tag.split('=')
                    mpd["bitrates"].append(int(kv[1]))
                    tmp_bps = int(kv[1])
                    mpd[tmp_bps] = []
        if "<Representation id" in line:
            if "audio" in line:
                continue
            stt = line.find('"')
            end = line.find('"', stt+1, len(line)-1)
            dir = line[stt+1:end]
            dirname = filename.split('/')
            dirname[-1] = dir
            dirname = '/'.join(dirname) + '/'
            mpd[tmp_bps] = fsize_edgesuite(dirname)
    mpd["bitrates"].sort()
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
    farray.append(8 * os.path.getsize(dirname + finit))
    i = 1
    while (True):
        fn = dirname + fp + str(i) + ".m4s"
        if os.path.exists(fn):
            # change byte to bit
            farray.append(8 * os.path.getsize(fn))
        else:
            break
        i = i + 1
    #print farray
    return farray

def fsize_edgesuite(dirname) :
    files = os.listdir(dirname)
    fp = ""
    finit = "Header.m4s"
    farray = []
    farray.append(8 * os.path.getsize(dirname + finit))
    i = 0
    while (True):
        fn = dirname + fp + str(i) + ".m4s"
        if os.path.exists(fn):
            # change byte to bit
            farray.append(8 * os.path.getsize(fn))
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
        if str(type(mpd[k])) == "<type 'list'>":
            print k, len(mpd[k])
    print mpd["bitrates"]
    print mpd["min_buffer"]
    print mpd["seglen"]
    print "500459", mpd[500459]
    print "891912", mpd[891912]
    print "1171990", mpd[1171990]
    #bitrates = mpd["bitrates"]
    #print mpd[bitrates[0]]
    #print mpd[bitrates[1]]
