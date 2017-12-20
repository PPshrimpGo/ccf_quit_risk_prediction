## 特征工程

#### entbase

- 原始特征
	- PROV，RGYEAR，HY，ZCZB，ETYPE，MPNUM，INUM，ENUM，FINZB，FSTINUM，TZINUM
- EID_TRANS EID后面的数字
- FIRST2ONEHOT EID之前的字母做onehot
- RANK特征
	- ENTBASE_MIN_RANK
- 统计特征
	- HY_ETYPE_MPNUM，HY_ETYPE_INUM，HY_ETYPE_FINZB，HY_ETYPE_FSTINUM
- 交叉特征
	- cross_entbase，IE_gap，IE_ratio

#### alter
- 统计特征
	- other_value ALTERNO列非05，27，A015的数值出现次数
	- alter_count 变更次数
	- alter_unique_count 唯一变更次数（表中有重复）
	- alter_diff_count alter_count - alter_unique_count
- ALTBE
- ALTERNO进行onehot
- alter_first_year
- alter_last_year_to_now

#### branch
- B_REYEAR
- branch_count 分支数
- sub_life 分支存活时间
- IFHOME 分支本省比率

#### invest
- BTYEAR
- BTBL_SUM
- BTBL_COUNT
- BTBL_RATIO
- invest_life_ratio

#### right
- RIGHTTYPE onehot
- right_last_year_to_now
- ASKDATE_Y 申请年份
- right_count

#### project
- DJDATE onehot
- project_count
- project_home_count

#### lawsuit
- lawsuit_LAWAMOUNT_sum
- lawsuit_LAWAMOUNT_count
- LAWDATE_Y

#### breakfaith
- breakfaith_first_year
- FBDATE_Y
- breakfaith_is_count

#### recruit
- recruit_last_month_to_now
- recruit_last_year
- recruit_last_year_to_now
- RECDATE_Y
- WZCODE onehot
- recruit_nums

#### qualification
- qualification_count

#### 时间特征
- first_invest_year_from_setup
- last_invest_year_from_setup
- first_right_year_from_setup
- last_right_year_from_setup
- mean_right_year_from_setup
- first_recruit_year_from_setup
- mean_recruit_year_from_setup
- first_alter_year_from_setup

## 模型参数

本方案采用了lightgbm作为机器学习模型，相关参数如下：

```
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
```

本方案实现了一个简单的5折bagging，具体代码在models.py中。