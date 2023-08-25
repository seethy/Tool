import optparse
import os

COORD = {0:"N",1:"NNE",2:"NE",3:"ENE",4:"E",5:"ESE",6:"SE",7:"SSE",8:"S",9:"SSW",10:"SW",11:"WSW",12:"W",13:"WNW",14:"NW",15:"NWN",16:"N"}
DATADIR = "data/"

def getCoord(orientation):
    co = int((orientation+11.25)/22.5)
    return COORD.get(co)
# 统计总次数
def getTotal():
    count = 0
    for root, dirs, files in os.walk(DATADIR):
        for datafile in files:
            datafp = open(os.path.join(root, datafile), 'r')
            for fp in datafp.readlines():
                fs = fp.split()
                time = fs[0].strip()
                if time != 'Time':
                    count = count + 1
            datafp.close()
    return count

def countby(coordlimit, hslimit, timelimit):
    count = 0
    for root, dirs, files in os.walk(DATADIR):
        for datafile in files:
            datafp = open(os.path.join(root, datafile), 'r')
            for fp in datafp.readlines():
                fs = fp.split()
                dirr = fs[3].strip()
                if dirr != "DIR":
                    hs = float(fs[4].strip())
                    tm10 = float(fs[6].strip())
                    coord = getCoord(float(dirr))
                    # filter condition
                    #if coord == coordlimit and (hs >= hslimit or tm10 >= timelimit):
                    if coord == coordlimit and (hs >= hslimit):
                        count = count + 1
            datafp.close()
    return count


if __name__=="__main__":
    mdopt = optparse.OptionParser()
    mdopt.add_option('-d', '--direction', dest='coord', type='string', default='', help='方向，如:SE')
    mdopt.add_option('-s', '--hs', dest='hs', type='float', default=0, help='水深临界值')
    mdopt.add_option('-t', '--time', dest='time', type='float', default=0, help='周期临界值')
    options, args = mdopt.parse_args()
    coordlimit = options.coord
    hslimit = options.hs
    timelimit = options.time
    print("args: %s,%f,%f" % (coordlimit, hslimit, timelimit))
    total = getTotal()
    statnum = countby(coordlimit, hslimit, timelimit)
    print("Total:%d, count by condition:%d" % (total, statnum))
    result = statnum/total
    print("Result:%f" % result)
