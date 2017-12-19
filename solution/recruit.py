import pandas as pd
from utils import *

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

def get_num(x):
    if isinstance(x, int) or isinstance(x, float):
        return x
    if x == "若干":
        return 1
    if "人" in x:
        return int(x.split("人")[0])
    return 0

def recruit():
    recruit = pd.read_csv('../public/9recruit.csv')
    output = pd.DataFrame()
    output['EID'] = recruit.groupby("EID").count().index

    recruit["recdate_month_gap"] = recruit["RECDATE"].apply(get_month_gap).astype(int)
    tmp = recruit.groupby("EID", as_index=False)["recdate_month_gap"].min()
    tmp.rename(columns={"recdate_month_gap": "recruit_last_month_to_now"}, inplace=True)
    output = pd.merge(output, tmp, on=["EID"], how="left")

    # 在main中使用
    recruit['RECDATE_Y'] = recruit['RECDATE'].apply(get_year).astype(int)
    recruit_first_year = recruit.groupby("EID", as_index=False)["RECDATE_Y"].min()
    recruit_first_year.rename(columns={"RECDATE_Y": "recruit_first_year"}, inplace=True)
    output = pd.merge(output, recruit_first_year, on=["EID"], how="left")
    recruit_mean_year = recruit.groupby("EID", as_index=False)["RECDATE_Y"].min()
    recruit_mean_year.rename(columns={"RECDATE_Y": "recruit_mean_year"}, inplace=True)
    output = pd.merge(output, recruit_mean_year, on=["EID"], how="left")
    recruit_last_year = recruit.sort_values('RECDATE_Y', ascending=False).drop_duplicates('EID')[['EID', 'RECDATE_Y']]
    recruit_last_year.rename(columns={"RECDATE_Y": "recruit_last_year"}, inplace=True)
    output = pd.merge(output, recruit_last_year, on=["EID"], how="left")
    output["recruit_last_year_to_now"] = output["recruit_last_year"].apply(lambda u: 2017-u)
    # output['recruit_range'] = output['recruit_last_year'] - output['recruit_first_year']

    tmp = pd.DataFrame(recruit[["EID", "RECDATE_Y"]]).drop_duplicates("EID")
    output = pd.merge(output, tmp, on=["EID"], how="left")

    recruit_WZCODE = pd.get_dummies(recruit['WZCODE'], prefix='WZCODE')
    recruit_WZCODE_merge = pd.concat([recruit['EID'], recruit_WZCODE], axis=1)
    recruit_WZCODE_info_sum = recruit_WZCODE_merge.groupby(['EID'], as_index=False).sum().drop_duplicates(['EID'])
    output = pd.merge(output, recruit_WZCODE_info_sum, on=["EID"], how="left")

    recruit["recruit_num"] = recruit["PNUM"].apply(get_num)
    recruit_nums = recruit.groupby("EID", as_index=False)["recruit_num"].sum()
    recruit_nums.rename(columns={"recruit_num": "recruit_nums"}, inplace=True)
    output = pd.merge(output, recruit_nums, on=["EID"], how="left")

    # print (output.columns)
    return output

if __name__ == "__main__":
    recruit()