import pandas as pd
from utils import *

def breakfaith():
    breakfaith = pd.read_csv('../public/8breakfaith.csv')
    output = pd.DataFrame()
    output["EID"] = breakfaith.groupby("EID").count().index

    breakfaith['FBDATE_Y'] = breakfaith['FBDATE'].apply(get_year).astype(int)
    breakfaith_first_year = breakfaith.sort_values('FBDATE_Y').drop_duplicates('EID')[['EID', 'FBDATE_Y']]
    breakfaith_first_year.rename(columns={'FBDATE_Y': 'breakfaith_first_year'}, inplace=True)
    output = pd.merge(output, breakfaith_first_year, on=["EID"], how='left')

    tmp = pd.DataFrame(breakfaith[["EID", "FBDATE_Y"]]).drop_duplicates("EID")
    output = pd.merge(output, tmp, on=["EID"], how="left")

    breakfaith['SXENDDATE'] = breakfaith['SXENDDATE'].fillna(0)
    breakfaith['is_breakfaith'] = breakfaith['SXENDDATE'] != 0
    breakfaith['is_breakfaith'] = breakfaith['is_breakfaith'].astype(int)
    breakfaith_is_count = breakfaith.groupby(['EID'], as_index=False)['is_breakfaith'].count()
    breakfaith_is_count.rename(columns={'is_breakfaith': 'breakfaith_is_count'}, inplace=True)
    output = pd.merge(output, breakfaith_is_count, on=["EID"], how="left")

    # print (output.describe())
    # print (output.shape)

    return output

if __name__ == "__main__":
    breakfaith()