from utils import *
import pandas as pd

def project():
    project = pd.read_csv('./public/6project.csv')
    output = pd.DataFrame()
    output["EID"] = project.groupby("EID").count().index

    project['DJDATE_Y'] = project['DJDATE'].apply(get_year).astype(int)
    project_DJDATE_Y = pd.get_dummies(project['DJDATE_Y'], prefix='DJDATE')
    project_DJDATE_Y_info = pd.concat([project['EID'], project_DJDATE_Y], axis=1)
    project_DJDATE_Y_info_sum = project_DJDATE_Y_info.groupby(['EID'], as_index=False).sum()
    project_DJDATE_Y_info_sum = project_DJDATE_Y_info_sum.drop_duplicates(['EID'])
    output = pd.merge(output, project_DJDATE_Y_info_sum, on=["EID"], how="left")

    project_count = project.groupby(['EID'], as_index=False)['DJDATE'].count()
    project_count.rename(columns={'DJDATE': 'project_count'}, inplace=True)
    output = pd.merge(output, project_count, on=["EID"], how="left")

    project_home_count = project.groupby(by=['EID'], as_index=False)['IFHOME'].sum()
    project_home_count.rename(columns={'IFHOME': 'project_home_count'}, inplace=True)
    output = pd.merge(output, project_home_count, on=["EID"], how="left")

    # print (output.describe())
    # print (output.shape)
    return output

if __name__ == "__main__":
    project()