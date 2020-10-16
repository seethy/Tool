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

    def getAllStock(self):
        rs = bs.query_all_stock(day="2021-11-05")
        datalist = []
        while rs.error_code == '0' and rs.next():
            datalist.append(rs.get_row_data())
        print("Get all stock size:%d" % len(datalist))
        result = pd.DataFrame(datalist, columns=rs.fields)
        result.to_csv("D:\\all_stock.csv", encoding="gbk", index=False)
        print(result)



if __name__ == '__main__':
    sm = StockModel()
    sm.login()
    sm.getAllStock()
    sm.logout()