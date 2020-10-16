# -*- coding: UTF-8 -*-
import math
import os
import datetime
#原始数据
datadir = "E:\\cauchy\\pywork\\Tool\\wave\\huafeng\\2015"
#保存数据文件
savefile = "E:\\cauchy\\pywork\\Tool\\wave\\huafeng\\save\\omit.txt"
#波高临界值
hstop = {"E":10.4,"ESE":2.5,"SE":2.2, "SSE":1.7,"S":3.0, "SSW":3.1}
#周期临界值
tmtop = 6
#风速临界值
wintop =15
coord = {0:"N",1:"NNE",2:"NE",3:"ENE",4:"E",5:"ESE",6:"SE",7:"SSE",8:"S",9:"SWS",10:"SW",11:"WSW",12:"W",13:"WNW",14:"NW",15:"NWN",16:"N"}
#统计每天发生的次数
dayaccurs = 1
daytimes = {}
savedayfile = "E:\\cauchy\\pywork\\Tool\\wave\\huafeng\\save\\daytimes4.txt"
directfile = "E:\\cauchy\\pywork\\Tool\\wave\\huafeng\\save\\direct-2015.txt"
#统计连续时间
daycontinuous = 0

def getCoord(orientation):
    co = int((orientation+11.25)/22.5)
    return coord.get(co)

def filehandler(file):
    fp = open(file, "r")
    for line in fp:
        fields = line.split()
        time = fields[0]
        day = time[0:8]
        #这里的day包括年月日，如：20170320，只要截取前面4位，就能获取到年份
        year = day[0:4]
        #这里加上判断，如果不是该年份，就退出
        if year != "2015" :
            continue
        hour = time[9:11]
        if time == "Time"or int(hour)%3 != 2:
            continue
        windx = float(fields[1])
        windy = float(fields[2])
        dir = float(fields[3])
        hs = float(fields[4])
        hswell = float(fields[5])
        tmm10 = float(fields[6])
        tps = float(fields[7])
        coord = getCoord(dir)
        hstopval = hstop.get(coord)

        win = math.sqrt(windx * windx + windy * windy)

        #for debug
       # if (hstopval != None and hs >= hstopval):
        #    print line.strip() + " hs|" + coord

        #output(line.strip() + " " + coord, directfile)

        if tmm10 >= tmtop:
           print line.strip() + " tm"
       # if win >= wintop:
       #     print line.strip() + " win|" + str(win)

        if tmm10 >= tmtop:
          #   (hstopval!=None and hs>=hstopval) :
            #print "%s,%.2f,%.2f,%.2f,%s,hs" % (time,windx,windy,win,coord)
            #or tmm10 >= tmtop or win >= wintop:
            if daytimes.has_key(day):
                daytimes[day] = daytimes[day] + 1
            else:
                daytimes[day] = 1
            #print line.strip()
            output(line.strip(),savefile)
    fp.close()

#统计每天发生的次数
def daytimeshandler():
    print "start handler day times..."
    daytimesarr = []
    for (k, v) in daytimes.items():
        if v >= dayaccurs:
            daytimesarr.append(k)
    daytimesarr.sort()
    for i in daytimesarr:
        output(i, savedayfile)
    #统计连续N天发生
    print "start handler day continuous..."
    stack=[]
    for i in daytimesarr:
        if len(stack) == 0 or isBetween1day(i,stack[len(stack)-1]):
            stack.append(i)
            continue
        if not isBetween1day(i,stack[len(stack)-1]):
            if len(stack) > daycontinuous:
                print stack
            stack = []

def isBetween1day(datestr1, datestr2):
    date1 = datetime.date(int(datestr1[0:4]),int(datestr1[4:6]),int(datestr1[6:8]))
    date2 = datetime.date(int(datestr2[0:4]),int(datestr2[4:6]),int(datestr2[6:8]))
    delta = datetime.timedelta(days=1)
    return date1-date2 == delta


def loopdir(path):
    print "start handler data..."
    if os.path.isdir(path):
        for p in os.listdir(path):
            filehandler(path + os.sep + p)

def output(str, path):
    fp = open(path,"a")
    fp.write(str+"\n")
    fp.close()


if __name__=="__main__":

    if os.path.exists(savefile):
        os.remove(savefile)
    if os.path.exists(savedayfile):
        os.remove(savedayfile)
    if os.path.exists(directfile):
        os.remove(directfile)
    loopdir(datadir)
    daytimeshandler()