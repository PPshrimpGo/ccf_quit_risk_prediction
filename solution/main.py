from utils import *
from models import *
from entbase import *
from alter import *
from branch import *
from invest import *
from right import *
from project import *
from lawsuit import *
from breakfaith import *
from recruit import *
from qualification import *
import pandas as pd
import numpy as np
import datetime
from itertools import combinations
from scipy.stats import spearmanr,pearsonr,skew,kurtosis,entropy



def get_data():
    train = pd.read_csv("../public/train.csv")

    entbase_ = entbase()
    train = merge(train, entbase_)
    print ("basic done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del entbase_

    alter_ = alter()
    train = merge(train, alter_)
    print("alter done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del alter_

    branch_=branch()
    train = merge(train, branch_)
    print("branch done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del branch_

    invest_=invest()
    train=merge(train,invest_)
    print("invest done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del invest_

    right_=right()
    train = merge(train, right_)
    print("right done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del right_

    project_=project()
    train = merge(train, project_)
    print("project done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del project_

    lawsuit_=lawsuit()
    train = merge(train, lawsuit_)
    print("lawsuit done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del lawsuit_

    breakfaith_=breakfaith()
    train = merge(train, breakfaith_)
    print("breakfaith done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del breakfaith_

    recruit_=recruit()
    train = merge(train, recruit_)
    print("recruit done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del recruit_

    qualification_ = qualification()
    train = merge(train, qualification_)
    print("qualification done in " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    del qualification_

    return train

def cross_feature(data):
    # 这个特征好像起副作用
    # data["first_alter_year_from_setup"] = data["alter_first_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    # data["first_branch_year_from_setup"] = data["branch_first_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]

    data["first_invest_year_from_setup"] = data["invest_first_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    data = data.drop(["invest_first_year"], axis=1)
    data["last_invest_year_from_setup"] = data["invest_last_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    data = data.drop(["invest_last_year"], axis=1)

    data["first_right_year_from_setup"] = data["right_first_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    data = data.drop(["right_first_year"], axis=1)
    data["last_right_year_from_setup"] = data["right_last_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    data = data.drop(["right_last_year"], axis=1)
    data["mean_right_year_from_setup"] = data["right_mean_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    data = data.drop(["right_mean_year"], axis=1)

    data["first_recruit_year_from_setup"] = data["recruit_first_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    data = data.drop(["recruit_first_year"], axis=1)
    data["mean_recruit_year_from_setup"] = data["recruit_mean_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    data = data.drop(["recruit_mean_year"], axis=1)

    data["first_alter_year_from_setup"] = data["alter_first_year"].fillna(data["RGYEAR"]) - data["RGYEAR"]
    # 不删，因为比较重要
    # data = data.drop(["recruit_alter_year"], axis=1)

    return data

def main():
    data = get_data()

    data = cross_feature(data)

    print('SSSSSSSSSSSSSSTTTTTTTTTTTTAAAAAAAARRRRRRRRRRTTTTTTTTTT')
    ts = data[pd.isnull(data["TARGET"])]
    tr = data[~pd.isnull(data['TARGET'])]

    # get y labels
    tr_y = pd.DataFrame()
    tr_y["TARGET"] = tr["TARGET"]

    cols = [u for u in tr.columns if u not in ["TARGET", "ENDDATE"]]
    tr = tr[cols]

    ts_ = pd.read_csv('../public/evaluation_public.csv')
    ts = pd.merge(ts_, ts, how='inner', on='EID')
    ts = ts[cols]

    tr.fillna(-999, inplace=True)
    ts.fillna(-999, inplace=True)

    print(tr.shape)
    for i in tr.columns:
        print (i)
    # tr.to_csv("tr.csv", index=False)
    print(tr_y.shape)
    # tr_y.to_csv("tr_y.csv", index=False)
    print(ts.shape)
    # ts.to_csv("ts.csv", index=False)
    print ("data prepared !!!")

    lgb_train(tr, tr_y["TARGET"], ts)


if __name__ == "__main__":
    np.random.seed(20171124)
    main()