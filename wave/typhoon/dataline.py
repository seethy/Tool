# -*- coding:utf-8 -*-
import os
import matplotlib.pyplot as plt
import datetime, time
import dbscan


datadirs = "D:\\workdir\\49-17new\\N1"
hslist = []
#t1=datetime.datetime.strptime("19490909.230000", "%Y%m%d.%H%M%S")
#t2=datetime.datetime.strptime("19490909.220000", "%Y%m%d.%H%M%S")

#print time.mktime((t1+datetime.timedelta(days=50*365)).timetuple())
#print time.mktime((t2+datetime.timedelta(days=50*365)).timetuple())

print "read data files ..."
pridata = {}
for root, dirs, files in os.walk(datadirs):
    for datafile in files:
        datafp = open(os.path.join(root, datafile), 'r')
        for fp in datafp.readlines():
            fs = fp.split()
            ti = fs[0].strip()
            hs = fs[4].strip()
            if ti != "Time" and ti != "":
                #hslist.append((time, float(hs)))
                ###数据清洗，将<5m的波高剔除掉
                if(float(hs) > 5):
                    hslist.append((datetime.datetime.strptime(ti, "%Y%m%d.%H%M%S"), float(hs)))
                    pridata[datetime.datetime.strptime(ti, "%Y%m%d.%H%M%S")] = fp.strip()
        datafp.close()


print len(hslist)    #325752s

def sortbytime(element):
    return element[0]

print "order data..."
###filter data from 1979
hslist.sort(key=sortbytime, reverse=False)
hsfilterlist = [e for e in hslist if time.mktime((e[0] + datetime.timedelta(days=50 * 365)).timetuple()) >= \
                time.mktime((datetime.datetime.strptime('19790101.000000', "%Y%m%d.%H%M%S") + datetime.timedelta(days=50 * 365)).timetuple())]
print hsfilterlist

#show pri filter scatter
#plt.scatter(zip(*hsfilterlist)[0], zip(*hsfilterlist)[1], marker='.')
#plt.show()



# show dbscan later
print "dbscan..."
c1, k = dbscan.my_dbscan(hsfilterlist, 72, 1)

print "print by order"
maxdict = dict.fromkeys(range(k), 0)
maxtmp = 0
scanresult = []
for d in range(0, len(hsfilterlist)):
    maxdict[c1[d]] = max(maxdict.get(c1[d]), hsfilterlist[d][1])
    print hsfilterlist[d][0], hsfilterlist[d][1], c1[d]
    scanresult.append((hsfilterlist[d][0], hsfilterlist[d][1], c1[d]))

print maxdict
print "=============sort by hsmax===================="

def sortbymax(element):
    return "%4.2f%s" % (maxdict.get(element[2]), element[0])
scanresult.sort(key=sortbymax, reverse=True)
tmp = -1
for i in range(len(scanresult)):
    if scanresult[i][2] != tmp:
        print "===========Group Id:%d, Max:%f======" % (scanresult[i][2], maxdict.get(scanresult[i][2]))
        tmp = scanresult[i][2]
    #print scanresult[i][0], scanresult[i][1], scanresult[i][2]
    print pridata[scanresult[i][0]]

print "figure out..."
plt.scatter(zip(*hsfilterlist)[0], zip(*hsfilterlist)[1], c=c1, marker='.')
plt.show()


'''
plt.plot(times, hss, 'ro')
plt.title('line chart')
plt.xlabel('time')
plt.ylabel('hs')
plt.show()
'''