import time

#返回当前日期格式串
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

if __name__=="__main__":
    print(now())