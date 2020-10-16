##
# 和鲸社区算法练习：「二分类算法」提供银行精准营销解决方案
# 逻辑回归
# 支持向量机
# K近邻
# 决策树等
##
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from algorithm.util import DateUtil


trainfile="train_set.csv"
testfile="test_set.csv"


def getdict(tf, pos):
    s = set(tf[:, pos])
    dict = {}
    for i in range(len(s)):
        dict[s.pop()] = i
    print(dict)
    return dict

def convert(dict, type):
    return dict[type]
###数据清洗，预处理
tf = np.loadtxt(trainfile, dtype=str, delimiter=',', skiprows=1, encoding='utf-8')
###第7个字段，balance归一化
#balance_max = max(tf[:, 6].astype(float), key=abs)

jobdict = getdict(tf, 2)
maritaldict = getdict(tf, 3)
educationdict = getdict(tf, 4)
defaultdict = getdict(tf, 5)
housingdict = getdict(tf, 7)
loandict = getdict(tf, 8)
contactdict = getdict(tf, 9)
poutcomedict = getdict(tf, 16)

#def balance(src):
#    return round(float(src)/balance_max,2)
def jobconvert(type):
    return jobdict[type]
def maritalconvert(type):
    return maritaldict[type]
def educationconvert(type):
    return educationdict[type]
def defaultconvert(type):
    return defaultdict[type]
def housingconvert(type):
    return housingdict[type]
def loanconvert(type):
    return loandict[type]
def contactconvert(type):
    return contactdict[type]
def poutcomeconvert(type):
    return poutcomedict[type]
# data = np.loadtxt(trainfile, dtype=int, delimiter=',', skiprows=1,
#                   converters={2:jobconvert,3:maritalconvert,4:educationconvert,5:defaultconvert,
#                               7:housingconvert,8:loanconvert,9:contactconvert,16:poutcomeconvert},
#                   usecols=(1,2,3,4,5,6,7,8,9,12,13,14,15,16,17), encoding='utf-8')

isprobability = True
data = np.loadtxt(trainfile, dtype=float, delimiter=',', skiprows=1,
                  converters={2:jobconvert,3:maritalconvert,4:educationconvert,5:defaultconvert,
                              7:housingconvert,8:loanconvert,9:contactconvert,16:poutcomeconvert},
                  usecols=(5,6,7,8,17), encoding='utf-8')
train_xdata, train_ydata = np.split(data, (4,), axis=1)   #pri:14
min_max_scaler = MinMaxScaler()
train_xdata = min_max_scaler.fit_transform(train_xdata)
train_ydata = min_max_scaler.fit_transform(train_ydata)
#print(train_xdata)
#print(train_ydata)
print("%s:Begin train" % DateUtil.now())
clf = svm.SVC(C=1, kernel='rbf', gamma=0.25, probability=isprobability, decision_function_shape='ovr')
clf.fit(train_xdata, train_ydata.ravel())
print("%s:Train success" % DateUtil.now())

#print(clf.score(train_xdata, train_ydata))  # 精度
test_xdata = np.loadtxt(testfile, dtype=float, delimiter=',', skiprows=1,
                  converters={2:jobconvert,3:maritalconvert,4:educationconvert,5:defaultconvert,
                              7:housingconvert,8:loanconvert,9:contactconvert,16:poutcomeconvert},
                  usecols=(5,6,7,8), encoding='utf-8')
test_xdata = min_max_scaler.fit_transform(test_xdata)
if isprobability:
    y_hat = clf.predict_proba(test_xdata)
else:
    y_hat = clf.predict(test_xdata)
test_id = np.loadtxt(testfile, dtype=float, delimiter=',', skiprows=1, usecols=0, encoding='utf-8')
print(y_hat)
print("%s:Test success" % DateUtil.now())

if isprobability:
    result = zip(test_id, y_hat[:,1])
else:
    result = zip(test_id, y_hat)
f = open('result.txt', 'w+')
for line in result:
    f.write("%s,%s\n" % (line[0], line[1]))
f.close()

#print clf.score(x_test, y_test)
#y_hat = clf.predict(x_test)