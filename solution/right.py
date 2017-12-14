from utils import *
import pandas as pd
import time
from scipy.stats import pearsonr
import datetime

def get_month_gap(df):
    try:
        if "-" in df:
            year = df.split('-')[0]
            month = df.split('-')[1]
            year_gap = 2017 - int(year)
            return 8 + 12 * year_gap - int(month)
        elif "/" in df:
            year = df.split('/')[0]
            month = df.split('/')[1]
            year_gap = 2017 - int(year)
            return 8 + 12 * year_gap - int(month)
        elif "年" in df:
            year = int(df.split("年")[0])
            month = int(df.split("年")[1].split("月")[0])
            year_gap = 2017 - int(year)
            return 8 + 12 * year_gap - int(month)
    except:
        return -1

def tm2unix(df):
    try:
        return time.mktime(datetime.datetime.strptime(str(df), '%Y-%m').timetuple())
    except:
        return -1

def trans(x):
    if "GXB" in x or "cno" in x or "mno" in x or "pno" in x:
        return int(x[3:])
    return int(x)

def first2onehot(x):
    if "GXB" in x:
        return 1
    elif "cno" in x:
        return 2
    elif "mno" in x:
        return 3
    elif "pno" in x:
        return 4
    else:
        return 5

def right():
    right = pd.read_csv('./public/5right.csv')
    output = pd.DataFrame()
    output["EID"] = right.groupby("EID").count().index

    right["type_code_trans"] = right["TYPECODE"].apply(trans)

    right["type_code_onehot"] = right["TYPECODE"].apply(first2onehot)

    right["right_askdate_month_gap"] = right["ASKDATE"].apply(get_month_gap).astype(int)
    right["right_fbdate_month_gap"] = right["FBDATE"].apply(get_month_gap).astype(int)
    right["right_apply_time"] = right["right_askdate_month_gap"] - right["right_fbdate_month_gap"]

    right_RIGHTTYPE = pd.get_dummies(right['RIGHTTYPE'], prefix='RIGHTTYPE')
    right_RIGHTTYPE_info = pd.concat([right['EID'], right_RIGHTTYPE], axis=1)
    right_RIGHTTYPE_info_sum = right_RIGHTTYPE_info.groupby(['EID'], as_index=False).sum().drop_duplicates(['EID'])
    output = pd.merge(output, right_RIGHTTYPE_info_sum, on=["EID"], how="left")

    # 在main使用
    right['ASKDATE_Y'] = right['ASKDATE'].apply(get_year).astype(int)
    right_first_year = right.groupby("EID", as_index=False)["ASKDATE_Y"].min()
    right_first_year.rename(columns={"ASKDATE_Y": "right_first_year"}, inplace=True)
    output = pd.merge(output, right_first_year, on=["EID"], how="left")
    right_last_year = right.sort_values('ASKDATE_Y', ascending=False).drop_duplicates('EID')[['EID', 'ASKDATE_Y']]
    right_last_year.rename(columns={'ASKDATE_Y': 'right_last_year'}, inplace=True)
    output = pd.merge(output, right_last_year, on=["EID"], how="left")
    output["right_last_year_to_now"] = output["right_last_year"].apply(lambda u: 2017-u)
    right_mean_year = right.groupby("EID", as_index=False)["ASKDATE_Y"].mean()
    right_mean_year.rename(columns={"ASKDATE_Y": "right_mean_year"}, inplace=True)
    output = pd.merge(output, right_mean_year, on=["EID"], how="left")
    # output['right_range'] = output['right_last_year'] - output['right_first_year']

    tmp = pd.DataFrame(right[["EID", "ASKDATE_Y"]]).drop_duplicates("EID")
    output = pd.merge(output, tmp, on=["EID"], how="left")
    # print (pearsonr(output["ASKDATE_Y"], output["right_last_year"]))

    right_count = right.groupby(['EID'], as_index=False)['RIGHTTYPE'].count()
    right_count.rename(columns={'RIGHTTYPE': 'right_count'}, inplace=True)
    output = pd.merge(output, right_count, on=["EID"], how="left")

    # print (output.describe())
    # print (output.shape)
    return output

if __name__ == "__main__":
    right()