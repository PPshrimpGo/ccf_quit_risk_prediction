import pandas as pd
import time
import datetime
from itertools import combinations

def process_time(df, col, mode='month'):
    # start time 2017-08
    def get_month_gap(df):
        try:
            year = df.split('-')[0]
            month = df.split('-')[1]
            year_gap = 2017-int(year)
            return 8 + 12 * year_gap - int(month)
        except:
            year = df.split('/')[0]
            month = df.split('/')[1]
            year_gap = 2017 - int(year)
            return 8 + 12 * year_gap - int(month)
    if mode == 'month':
        df[col + '_month_gap'] = df[col].apply(lambda x:get_month_gap(x))
    elif mode == 'year':
        df[col + '_year_gap'] = df[col].apply(lambda x: 2017-int(x))

def get_year(df):
    try:
        if "-" in df:
            year = df.split('-')[0]
            return year
        elif "/" in df:
            year = df.split('/')[0]
            return year
        elif "年" in df:
            year = df.split("年")[0]
            return year
    except:
        return -1

# To checkout the company is close or not
def is_close(df):
    if pd.isnull(df):
        return 0
    else:
        return 1

def tm2unix(df):
    try:
        return time.mktime(datetime.datetime.strptime(str(df), '%Y-%m').timetuple())
    except:
        return -1

# merge two tables together
def merge(df1,df2):
    return pd.merge(df1, df2, on='EID', how='outer')

# 去除缺失值过多的列
def drop_miss(df, pass_cols=['TARGET'], ratio=0.95):
    out = []
    for x in df.columns:
        if x in pass_cols:
            continue
        stats_num = df[x].shape[0]
        miss_num = sum(pd.isnull(df[x]))
        if miss_num / float(stats_num) > ratio:
            out.append(x)
    return out

def encode_(df):
    if df!=-1:
        return 1
    else:
        return 0


