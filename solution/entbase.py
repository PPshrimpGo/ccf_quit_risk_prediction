from utils import *
import pandas as pd
from scipy.stats import spearmanr,pearsonr,skew,kurtosis,entropy
from itertools import combinations
import numpy as np

def mpnum_trans(dd):
    if dd > 4:
        return 4
    return dd

def inum_trans(dd):
    if dd > 3:
        return 3
    return dd

def finzb_trans(dd):
    if dd == 0:
        return 0
    return 1

def fstinum_trans(dd):
    if dd > 4:
        return 4
    return dd

def tzinum_trans(dd):
    if dd == 0:
        return 0
    return 1

def eid_trans(x):
    return int(x[1:])

def first2onehot(x):
    if x[0] == "p":
        return 0
    elif x[0] == 's':
        return 1
    else:
        return 2

def after1978(x):
    if x >= 1978:
        return 1
    else:
        return 0

def entbase():
    entbase = pd.read_csv('../public/1entbase.csv')
    entbase = entbase.fillna(0.0)
    entbase['EID_TRANS'] = entbase['EID'].apply(eid_trans)
    entbase['FIRST2ONEHOT'] = entbase["EID"].apply(first2onehot)
    
    entbase['ENTBASE_MIN_RANK'] = (entbase[['TZINUM', 'MPNUM', "ENUM", 'INUM', 'FINZB', 'FSTINUM']].fillna(0.0).rank() / entbase.shape[0]).min(axis=1)

    for num in ['MPNUM', 'INUM', 'FINZB', 'FSTINUM']:  # 'EID_RANK','ENTBASE_SUM','ENTBASE_SUM_RANK'
        tmp = entbase.groupby(['HY', 'ETYPE'])[num].mean().reset_index()
        tmp.columns = ['HY', 'ETYPE', 'HY_ETYPE_' + num]
        entbase = pd.merge(entbase, tmp, on=['HY', 'ETYPE'], how='left')

    entbase['cross_entbase'] = entbase['ZCZB'] / (entbase['FINZB'].astype(float) + 1.0)
    
    entbase['IE_gap'] = entbase['INUM'] - entbase['ENUM']
    entbase['IE_ratio'] = (entbase['INUM'] - entbase['ENUM']) / (entbase['ENUM'] * 1.0 + 1.0)
    return entbase

if __name__ == "__main__":
    entbase()
