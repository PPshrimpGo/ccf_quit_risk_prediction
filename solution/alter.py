from utils import *
import pandas as pd
import numpy as np

def get_number(x):
    u = list(filter(str.isdigit,str(x)))
    lgh = len(u)
    if lgh == 0:
        return 0.0
    ot =float(u[0])
    if lgh >= 2:
        for x in u[1:]:
            ot = ot * 10 + float(x)
        return float(ot)
    return float(ot)

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

def other_value(x):
    if x in ["05", "27", "A015"]:
        return 0
    else:
        return 1

def clean(x):
    if x == 'null万元':
        return '0.0'
    return x

def alter():
    alter = pd.read_csv('../public/2alter.csv')
    alter = alter.fillna(0)
    output = pd.DataFrame()
    output["EID"] = alter.groupby("EID").count().index

    alter["other_value"] = alter["ALTERNO"].apply(other_value)
    alter_other_value = alter.groupby("EID", as_index=False)["other_value"].sum()
    output = pd.merge(output, alter_other_value, on=["EID"], how="left")

    # 变更次数
    alter_count = alter.groupby("EID", as_index=False)['ALTERNO'].count()
    alter_count.rename(columns={"ALTERNO": "alter_count"}, inplace=True)
    output = pd.merge(output, alter_count, on=["EID"], how="right")
    # unique 变更次数
    alter_count = alter.drop_duplicates().groupby("EID", as_index=False)['ALTERNO'].count()
    alter_count.rename(columns={"ALTERNO": "alter_unique_count"}, inplace=True)
    output = pd.merge(output, alter_count, on=["EID"], how="right")
    output["alter_diff_count"] = output["alter_count"] - output["alter_unique_count"]
    # output = output.drop(["alter_count", "alter_unique_count"], axis=1)
    # print (output.describe())

    ALTERNO_to_index = list(alter['ALTERNO'].unique())
    # 1 2 有金钱变化
    alter['ALTERNO'] = alter['ALTERNO'].map(ALTERNO_to_index.index)
    alter['ALTAF'] = np.log1p(alter['ALTAF'].map(lambda x: get_number(x)))
    # print (alter["ALTAF"].describe())
    alter['ALTBE'] = np.log1p(alter['ALTBE'].map(lambda x: get_number(x)))
    # print (alter['ALTBE'].describe())
    alter['ALTAF_ALTBE'] = alter['ALTAF'] - alter['ALTBE']

    alter['ALTDATE_YEAR'] = alter['ALTDATE'].map(lambda x: x.split('-')[0])
    alter['ALTDATE_YEAR'] = alter['ALTDATE_YEAR'].astype(int)
    alter['ALTDATE_MONTH'] = alter['ALTDATE'].map(lambda x: x.split('-')[1])
    alter['ALTDATE_MONTH'] = alter['ALTDATE_MONTH'].astype(int)

    alter = alter.sort_values(['ALTDATE_YEAR', 'ALTDATE_MONTH'], ascending=True)
    alter_ALTERNO = pd.get_dummies(alter['ALTERNO'], prefix='ALTERNO')
    alter_ALTERNO_merge = pd.concat([alter[['EID',"ALTBE"]], alter_ALTERNO], axis=1)
    alter_ALTERNO_info_sum = alter_ALTERNO_merge.groupby(['EID'], as_index=False).sum()

    alter_ALTERNO_info = pd.merge(alter_ALTERNO_info_sum, alter[['EID']], on=['EID']).drop_duplicates(['EID'])
    alter_ALTERNO_info = alter_ALTERNO_info.fillna(-1)
    output = pd.merge(output, alter_ALTERNO_info, on=["EID"], how="left")

    # 第一个 表上变更 的发生年份
    alter_first_year = pd.DataFrame(alter[['EID', 'ALTDATE_YEAR']]).drop_duplicates(['EID'])
    alter_first_year.rename(columns={"ALTDATE_YEAR": "alter_first_year"}, inplace=True)
    output = pd.merge(output, alter_first_year, on=["EID"], how="left")
    # 最后一个 变更 的发生年份
    alter_last_year = pd.DataFrame(alter[['EID', 'ALTDATE_YEAR']]).sort_values(['ALTDATE_YEAR'],ascending=False).drop_duplicates(['EID'])
    alter_last_year.rename(columns={"ALTDATE_YEAR": "alter_last_year"}, inplace=True)
    output = pd.merge(output, alter_last_year, on=["EID"], how="left")
    output["alter_last_year_to_now"] = output["alter_last_year"].apply(lambda u: 2017-u)
    # output['alter_range'] = output['alter_last_year'] - output['alter_first_year']
    output = output.drop(["alter_last_year"], axis=1)

    return output

if __name__ == "__main__":
    alter()