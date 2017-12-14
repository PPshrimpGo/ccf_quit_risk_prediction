################
# This file is used for train different mpodels
# input parameters:
#   tr : train features
#   tr_y : train labels
#   df_ts : test features
# output parameters:
#   there is no output, but the results will be store at train_5_folder.csv && test_5_folder.csv
###############
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import cross_val_score,StratifiedKFold
import datetime
import numpy as np

def train_xgb_bagging(X, y, X_val,y_val,params):
    #X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15)
    xg_train = xgb.DMatrix(X, label=y)
    xg_val = xgb.DMatrix(X_val, label=y_val)
    watchlist  = [(xg_train,'train'), (xg_val,'eval')]
    clr = xgb.train(params, xg_train, params['num_rounds'], watchlist,
                    early_stopping_rounds=150, verbose_eval = 50)
    # xg_train = xgb.DMatrix(X, label=y)
    # clr = xgb.train(params, xg_train, params['num_rounds'])
    return clr

def xgb_train(tr,tr_y,df_ts):
    """
    :param tr: (n,m) n--sample nums, m--feature nums
    :param tr_y: (n,)
    :param df_ts: (k,m)
    :return:
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    from sklearn.metrics import roc_auc_score
    auc = []

    ### xgb parameters
    params = {}
    params['objective'] = 'binary:logistic'
    params['eval_metric'] = 'auc'
    # params['num_class'] = n_class
    params['eta'] = 0.012
    params['max_depth'] = 7
    params['subsample'] = 0.75
    params['colsample_bytree'] = 0.75
    #params['min_child_weight'] = 1
    params['silent'] = 1
    params['num_rounds'] = 3000
    params['scale_pos_weight']=3.5
    params['min_child_weight '] = 5

    f_cols = [u for u in tr.columns if u != "EID"]
    print ("stacking start at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    tr_res = pd.DataFrame()
    ts_res = pd.DataFrame()
    cols = []
    for i, (train_idx, test_idx) in enumerate(skf.split(tr, tr_y)):
        print ("fold " + str(i) + " start at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        train = tr.iloc[train_idx]
        train_y = tr_y.iloc[train_idx]
        eval = tr.iloc[test_idx]
        eval_y = tr_y.iloc[test_idx]
        gbm = train_xgb_bagging(train[f_cols], train_y, eval[f_cols], eval_y, params)

        eval_prob = gbm.predict(xgb.DMatrix(eval[f_cols]))
        eval_prob_df = pd.DataFrame(eval_prob, columns=["PROB"])
        eval_prob_df["EID"] = eval["EID"]
        tr_res = pd.concat([tr_res, eval_prob_df])

        test_prob = gbm.predict(xgb.DMatrix(df_ts[f_cols]))
        test_prob_df = pd.DataFrame(test_prob, columns=["PROB"+str(i)])
        ts_res = pd.concat([ts_res, test_prob_df], axis=1)
        cols.append("PROB"+str(i))

        auc.append(roc_auc_score(eval_y, eval_prob))
    print (auc)
    print("the mean auc is " + str(np.mean(auc)))

    # print (tr_res.shape)
    tr_res.to_csv("train_5_floder.csv", index=False)

    def cut(x):
        if x < 0.25:
            return 0
        else:
            return 1

    ts_res["PROB"] = ts_res[cols].mean(axis=1)

    to_save = pd.DataFrame()
    to_save["EID"] = df_ts["EID"]
    to_save["FORTARGET"] = ts_res["PROB"].apply(lambda u: cut(u))
    to_save["PROB"] = ts_res["PROB"]

    to_save.to_csv("test_5_floder.csv", index=False)

def train_lgb_bagging(X, y, X_val,y_val,params):
    lgb_train = lgb.Dataset(X, y)
    lgb_eval = lgb.Dataset(X_val, y_val, reference=lgb_train)

    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=2500,
                    valid_sets=lgb_eval,
                    early_stopping_rounds=150,
                    verbose_eval=50)
    return gbm

def lgb_train(tr,tr_y,df_ts):
    """
    :param tr: (n,m) n--sample nums, m--feature nums
    :param tr_y: (n,)
    :param df_ts: (k,m)
    :return:
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    from sklearn.metrics import roc_auc_score
    auc = []

    ### xgb parameters
    params = {
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': {'auc'},
        'num_leaves': 96,
        'learning_rate': 0.008,
        'feature_fraction': 0.75,
        'bagging_fraction': 0.7,
        'bagging_freq': 10,
        'verbose': 0
    }
    f_cols = [u for u in tr.columns if u != "EID"]
    print("stacking start at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    tr_res = pd.DataFrame()
    ts_res = pd.DataFrame()
    cols = []
    for i, (train_idx, test_idx) in enumerate(skf.split(tr, tr_y)):
        print("fold " + str(i) + " start at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        train = tr.iloc[train_idx]
        train_y = tr_y.iloc[train_idx]
        eval = tr.iloc[test_idx]
        eval_y = tr_y.iloc[test_idx]
        gbm = train_lgb_bagging(train[f_cols], train_y, eval[f_cols], eval_y, params)

        model = gbm
        gain = model.feature_importance('gain')
        ft = pd.DataFrame({'feature': model.feature_name(), 'split': model.feature_importance('split'),
                           'gain': 100 * gain / gain.sum()}).sort_values('gain', ascending=False)
        ft.to_csv('importance' + str(i) + '.csv')

        eval_prob = gbm.predict(eval[f_cols])
        eval_prob_df = pd.DataFrame(eval_prob, columns=["PROB"])
        eval_prob_df["EID"] = eval["EID"]
        tr_res = pd.concat([tr_res, eval_prob_df])

        test_prob = gbm.predict(df_ts[f_cols])
        test_prob_df = pd.DataFrame(test_prob, columns=["PROB" + str(i)])
        ts_res = pd.concat([ts_res, test_prob_df], axis=1)
        cols.append("PROB" + str(i))

        auc.append(roc_auc_score(eval_y, eval_prob))
    print(auc)
    print("the mean auc is " + str(np.mean(auc)))

    # print (tr_res.shape)
    tr_res.to_csv("train_5_floder.csv", index=False)

    def cut(x):
        if x < 0.25:
            return 0
        else:
            return 1

    ts_res["PROB"] = ts_res[cols].mean(axis=1)

    to_save = pd.DataFrame()
    to_save["EID"] = df_ts["EID"]
    to_save["FORTARGET"] = ts_res["PROB"].apply(lambda u: cut(u))
    to_save["PROB"] = ts_res["PROB"]

    to_save.to_csv("test_5_floder.csv", index=False)