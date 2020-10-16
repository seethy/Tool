# -*- coding: utf-8 -*-
###
###  居民消费价格指数
###
import pandas as pd
import cufflinks as cf


cf.set_config_file(offline=True)

df = pd.read_csv('consumers.csv', index_col=u'指标', encoding='GBK')
print(df)
#df.drop(0, axis=0)
#df_new = df.drop(labels=[u'指标'], axis=1)
df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)  # 转置
df2.sort_index(ascending=True, inplace=True) # 排序
print(df2)



df2.iplot(kind='scatter', xTitle='月份', yTitle='居民消费价格指数(上年同月=100)')

# cf.datagen.lines(1,500).ta_plot(study='sma',periods=[13,21,55])


# print df.shaped

