import pandas as pd
from utils import *
import numpy as np

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

def lawsuit():
    lawsuit = pd.read_csv('../public/7lawsuit.csv')
    output = pd.DataFrame()
    output["EID"] = lawsuit.groupby("EID").count().index

    lawsuit_LAWAMOUNT_sum = lawsuit.groupby(['EID'], as_index=False)['LAWAMOUNT'].sum()
    lawsuit_LAWAMOUNT_sum.rename(columns={'LAWAMOUNT': 'lawsuit_LAWAMOUNT_sum'}, inplace=True)
    lawsuit_LAWAMOUNT_sum['lawsuit_LAWAMOUNT_sum'] = np.log1p(lawsuit_LAWAMOUNT_sum['lawsuit_LAWAMOUNT_sum'])
    lawsuit_LAWAMOUNT_sum['lawsuit_LAWAMOUNT_sum'] = lawsuit_LAWAMOUNT_sum['lawsuit_LAWAMOUNT_sum'].astype(int)
    output = pd.merge(output, lawsuit_LAWAMOUNT_sum, on=["EID"], how="left")

    lawsuit_LAWAMOUNT_count = lawsuit.groupby(['EID'], as_index=False)['LAWAMOUNT'].count()
    lawsuit_LAWAMOUNT_count.rename(columns={'LAWAMOUNT': 'lawsuit_LAWAMOUNT_count'}, inplace=True)
    output = pd.merge(output, lawsuit_LAWAMOUNT_count, on=["EID"], how="left")

    lawsuit['LAWDATE_Y'] = lawsuit['LAWDATE'].apply(get_year).astype(int)
    
    tmp = pd.DataFrame(lawsuit[["EID", "LAWDATE_Y"]]).drop_duplicates("EID")
    output = pd.merge(output, tmp, on=["EID"], how="left")
    return output

if __name__ == "__main__":
    lawsuit()