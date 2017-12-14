from utils import *
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def branch():
    branch = pd.read_csv('./public/3branch.csv')
    output = pd.DataFrame()
    output["EID"] = branch.groupby("EID").count().index

    tmp = pd.DataFrame(branch[["EID", "B_REYEAR"]]).drop_duplicates("EID")
    output = pd.merge(output, tmp, on=["EID"], how="left")

    branch['B_ENDYEAR'] = branch['B_ENDYEAR'].fillna(branch['B_REYEAR'])
    branch['sub_life'] = branch['B_ENDYEAR'].fillna(branch['B_REYEAR']) - branch['B_REYEAR']
    branch = branch[branch['sub_life'] >= 0]
    branch_count = branch.groupby(['EID'], as_index=False)['TYPECODE'].count()
    branch_count.rename(columns={'TYPECODE': 'branch_count'}, inplace=True)
    output = pd.merge(output, branch_count, on=["EID"], how="left")

    branch = pd.merge(branch, branch_count, on=['EID'], how='left')
    branch['branch_count'] = np.log1p(branch['branch_count'])
    branch['branch_count'] = branch['branch_count'].astype(int)
    branch['sub_life'] = branch['sub_life'].replace({0.0: -1})

    home_prob = branch.groupby(by=['EID'])['IFHOME'].sum() / branch.groupby(by=['EID'])['IFHOME'].count()
    home_prob = home_prob.reset_index()
    branch = pd.DataFrame(branch[['EID', 'sub_life']]).drop_duplicates('EID')
    branch = pd.merge(branch, home_prob, on=['EID'], how='left')
    output = pd.merge(output, branch, on=["EID"], how="left")

    # print (output.describe())
    # print (output.shape)
    return output

if __name__ == "__main__":
    branch()