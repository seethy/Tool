import baostock as bs
import pandas as pd

class StockModel():
    def __init__(self):
        pass

    def login(self):
        bl = bs.login()
        if bl.error_code == '0':
            print("login baostock success")
        else:
            print("login baostock failure")

    def logout(self):
        bs.logout()
        print("baostock logout!")

    # 获取沪股和深股的所有上市公司的证券编码，过滤掉指数部分
    def getSHStock(self, day):
        rs = bs.query_all_stock(day=day)
        datalist = []
        while rs.error_code == '0' and rs.next():
            row = rs.get_row_data()
            if row[0].find("sh.6") >= 0 or row[0].find("sz.00") >= 0 or row[0].find("sz.30") >= 0:
                datalist.append(row[0])
        print("Get all shanghai stock size:%d" % len(datalist))
        #print(datalist)
        return datalist
        #result = pd.DataFrame(datalist, columns=rs.fields)
        #result.to_csv("D:\\all_stock.csv", encoding="gbk", index=False)
        #print(result)

    def filterStock(self, code):
        print("code:%s" % code)
        currdate = "2021-12-10"
        # 为了计算量比，开始时间必须是过去5个交易日。
        # turn:换手率;pctChg:涨幅; peTTM:市盈率；
        rs = bs.query_history_k_data_plus(code, "date,code,volume,turn,pctChg,peTTM",
                                          start_date='2021-12-03', end_date='2021-12-10',
                                          frequency="d", adjustflag="3")
        volumepast = 0
        count = 0
        while (rs.error_code == '0') & rs.next():
            row = rs.get_row_data()
            if row[2] == '':
                continue
            if row[0] != currdate and row[2] != '':
                volumepast = volumepast + int(row[2])
                count = count + 1
            else:
                volrate = int(row[2])/(volumepast/count) if volumepast>0 else 1
                #print("volrate:%s" % volrate)
                # 1<量比<10;5<换手率<10; 2<涨幅<5; 10<市盈率<30;
                if volrate>1 and volrate<10 and float(row[3]) > 5 and float(row[3]) < 10 and float(row[4])>2 and float(row[4])<5 and float(row[5])>10 and float(row[5])<30:
                    return True
                else:
                    return False


if __name__ == '__main__':
    sm = StockModel()
    sm.login()
    chosenlist = []
    stocklist = sm.getSHStock("2021-12-10")
    for stock in stocklist:
        if sm.filterStock(stock) is True:
            chosenlist.append(stock)

    print("chosen stock:")
    for s in chosenlist:
        print("%s\t" % s)
    sm.logout()