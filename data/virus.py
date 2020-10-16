import time
import json
import pandas as pd
import numpy as np
from datetime import datetime
from requests_html import HTMLSession


session = HTMLSession()
url = r'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
r = session.get(url).json()
data = json.loads(r['data'])
print(data.keys())
# 国内总量
print(data['chinaTotal'])
# 国内新增
print(data['chinaAdd'])
# 更新时间
print(data['lastUpdateTime'])
# 文章列表
print(data['articleList'])