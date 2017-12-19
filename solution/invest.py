from utils import *
import pandas as pd

def invest():
    invest = pd.read_csv('../public/4invest.csv')
    output = pd.DataFrame()
    output["EID"] = invest.groupby("EID").count().index

    tmp = pd.DataFrame(invest[["EID", "BTYEAR"]]).drop_duplicates("EID")
    output = pd.merge(output, tmp, on=["EID"], how="left")

    invest['BTENDYEAR'] = invest['BTENDYEAR'].fillna(invest['BTYEAR'])
    invest['invest_life'] = invest['BTENDYEAR'] - invest['BTYEAR']
    invest_BTBL_sum = invest.groupby(['EID'], as_index=False)['BTBL'].sum()
    invest_BTBL_sum.rename(columns={'BTBL': 'BTBL_SUM'}, inplace=True)
    invest_BTBL_count = invest.groupby(['EID'], as_index=False)['BTBL'].count()
    invest_BTBL_count.rename(columns={'BTBL': 'BTBL_COUNT'}, inplace=True)
    BTBL_INFO = pd.merge(invest_BTBL_sum, invest_BTBL_count, on=['EID'], how='left')
    BTBL_INFO['BTBL_RATIO'] = BTBL_INFO['BTBL_SUM'] / BTBL_INFO['BTBL_COUNT']
    output = pd.merge(output, BTBL_INFO, on=["EID"], how="left")

    invest['invest_life'] = invest['invest_life'] > 0
    invest['invest_life'] = invest['invest_life'].astype(int)
    invest_life_ratio = invest.groupby(['EID'])['invest_life'].sum() / invest.groupby(['EID'])['invest_life'].count()
    invest_life_ratio = invest_life_ratio.reset_index()
    invest_life_ratio.rename(columns={'invest_life': 'invest_life_ratio'}, inplace=True)
    output = pd.merge(output, invest_life_ratio, on=["EID"], how="left")

    # 在main里面用
    invest_last_year = invest.sort_values('BTYEAR', ascending=False).drop_duplicates('EID')[['EID', 'BTYEAR']]
    invest_last_year.rename(columns={"BTYEAR": "invest_last_year"}, inplace=True)
    output = pd.merge(output, invest_last_year, on=["EID"], how="left")
    invest_first_year = invest.sort_values('BTYEAR').drop_duplicates('EID')[['EID', 'BTYEAR']]
    invest_first_year.rename(columns={"BTYEAR": "invest_first_year"}, inplace=True)
    output = pd.merge(output, invest_first_year, on=["EID"], how="left")

    # print (output.describe())
    # print (output.shape)
    return output

if __name__ == "__main__":
    invest()