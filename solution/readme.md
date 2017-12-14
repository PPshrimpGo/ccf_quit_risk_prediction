# 2017/11/22

目前用50个左右的特征

```
50 features lgb
[0.68290867761661234, 0.67718064682237356, 0.68213944740397814, 0.68335683673995162, 0.68905907677081002]

50 features xgb
[0.67588667012386971, 0.67728229581032873, 0.67852524925485991, 0.68474159315792515, 0.68293094265798093]
```

#### 1entbase
```
全部原始特征，填充0
# entbase['zhuce'] = 2017 - entbase["RGYEAR"]
# 这些RANK特征起反作用
# entbase['ENTBASE_SUM_RANK'] = (entbase[['TZINUM', 'MPNUM', 'INUM', 'FINZB', 'FSTINUM']].fillna(0.0).rank() / entbase.shape[0]).sum(axis=1)
# entbase['ENTBASE_MEAN_RANK'] = (entbase[['TZINUM', 'MPNUM', 'INUM', 'FINZB', 'FSTINUM']].fillna(0.0).rank() / entbase.shape[0]).mean(axis=1)
# entbase['ENTBASE_MEDIAN_RANK'] = (entbase[['TZINUM', 'MPNUM', 'INUM', 'FINZB', 'FSTINUM']].fillna(0.0).rank() / entbase.shape[0]).median(axis=1)
# entbase['ENTBASE_MIN_RANK'] = (entbase[['TZINUM', 'MPNUM', 'INUM', 'FINZB', 'FSTINUM']].fillna(0.0).rank() / entbase.shape[0]).min(axis=1)
# entbase['ENTBASE_MAX_RANK'] = (entbase[['TZINUM', 'MPNUM', 'INUM', 'FINZB', 'FSTINUM']].fillna(0.0).rank() / entbase.shape[0]).max(axis=1)

"""
反作用反作用
rank_list = ["HY", "RGYEAR", "ETYPE", "ZCZB", "TZINUM", "MPNUM", "INUM", "FINZB", "FSTINUM"]
for e in rank_list:
    entbase["ENTBASE_" + e + "_RANK"] = entbase[e].rank()
"""
#entbase["MPNUM_TRANS"] = entbase["MPNUM"].apply(mpnum_trans)
#entbase["INUM_TRANS"] = entbase["INUM"].apply(inum_trans)
#entbase["FINZB_TRANS"] = entbase["FINZB"].apply(finzb_trans)
#entbase["FSTINUM_TRANS"] = entbase["FSTINUM"].apply(fstinum_trans)
#entbase["TZINUM_TRANS"] = entbase["TZINUM"].apply(tzinum_trans)

"""
没啥用，不提升也不降
for num in ['ZCZB', 'MPNUM', 'INUM', 'FINZB', 'FSTINUM']:  # 'EID_RANK','ENTBASE_SUM','ENTBASE_SUM_RANK'
    tmp = entbase.groupby(['HY', 'ETYPE'])[num].mean().reset_index()
    tmp.columns = ['HY', 'ETYPE', 'HY_ETYPE_' + num]
    entbase = pd.merge(entbase, tmp, on=['HY', 'ETYPE'], how='left')
"""

"""
特征变得超级多，还变差
agg_cats = ['RGYEAR', 'HY', 'ETYPE']
agg_nums = ['ZCZB', 'MPNUM', 'INUM', 'FINZB', 'FSTINUM']  # 'EID_RANK','ENTBASE_SUM'
for cat in agg_cats:
    for num in agg_nums:
        entbase[cat + '2' + num + '_MEAN'] = entbase[cat].map(entbase.groupby(cat)[num].mean())
        entbase[cat + '2' + num + '_STD'] = entbase[cat].map(entbase.groupby(cat)[num].std())
        entbase[cat + '2' + num + '_SKEW'] = entbase[cat].map(entbase.groupby(cat)[num].skew())
        entbase[cat + '2' + num + '_KURT'] = entbase[cat].map(
            entbase.groupby(cat)[num].aggregate({'KURT': kurtosis})['KURT'])
        entbase[cat + '2' + num + '_ENTROPY'] = entbase[cat].map(
            entbase.groupby(cat)[num].aggregate({'ENTROPY': entropy})['ENTROPY'])
        entbase[cat + '2' + num + '_SIZE'] = entbase[cat].map(entbase.groupby(cat)[num].size())

        entbase[cat + '2' + num + '_MEAN_RATIO'] = entbase[num] / entbase[cat + '2' + num + '_MEAN']
        entbase[cat + '2' + num + '_STD_RATIO'] = entbase[num] / entbase[cat + '2' + num + '_STD']
        entbase[cat + '2' + num + '_SKEW_RATIO'] = entbase[num] / entbase[cat + '2' + num + '_SKEW']

        entbase[cat + '2' + num + '_MEAN_DIFF'] = entbase[num] - entbase[cat + '2' + num + '_MEAN']
        entbase[cat + '2' + num + '_STD_DIFF'] = entbase[num] - entbase[cat + '2' + num + '_STD']
        entbase[cat + '2' + num + '_SKEW_DIFF'] = entbase[num] - entbase[cat + '2' + num + '_SKEW']
"""

"""
变差变差
fe = [item for item in entbase.columns if item not in ['TARGET', "ENDDATE"]]
entbase['BASE_NA_MEAN'] = entbase[fe].isnull().mean(axis=1)

entbase['BASE_ZERO_MEAN'] = (entbase[fe] == 0.0).mean(axis=1)

entbase['BASE_MISSING_CNT'] = entbase['BASE_NA_MEAN'] + entbase['BASE_ZERO_MEAN']
"""
```

#### 2alter
```
alter_count 变更发生次数
alter_unique_count 去重后变更发生次数（感觉需要跟时间结合，单独没啥意义）
*alter_diff_count

*对ALTERNO进行onehot
[ALTERNO_0, ALTERNO_1, ALTERNO_2, ALTERNO_3, ALTERNO_4, ALTERNO_5, ALTERNO_6, ALTERNO_7, ALTERNO_8, ALTERNO_9, ALTERNO_10, ALTERNO_11]

ALTAF_ALTBE 第一次变更变化（取对数减）[这个好像起副作用]( 已去除)

alter_first_year 第一个 表上变更 的发生年份
alter_last_year 最后一个 表上变更 的发生年份
*alter_last_year_to_now 最后一次变更距今几年
```

#### 3branch
```
branch_count 分支数目

sub_life 第一个 表上分支 的存活时间
*B_REYEAR 第一个 表上分支 的创建年份[不明白为什么，但是挺有用]

branch_first_year 第一个分支的创建年份
branch_last_year 最后一个分支的创建年份
branch_last_year_to_now 
[这三个特征都不是很重要，和alter表没法比，可以不用]

IFHOME 分支本省比率
```

#### 4invest
```
BTBL_SUM 持股总和

BTBL_COUNT 持股公司数

BTBL_RATIO 持股平均比例

invest_life_ratio 持股平均比例
```

#### 5right

```
onthot(RIGHTTYPE)
RIGHTTYPE_11, RIGHTTYPE_12, RIGHTTYPE_20, RIGHTTYPE_30, RIGHTTYPE_40, RIGHTTYPE_50, RIGHTTYPE_60

right_first_year[没啥用貌似]
right_last_year 

*ASKDATE_Y 第一个 表上权利 申请年份[不知道为啥，非常有用]

right_count

right_askdate_month_gap 申请时间到现在的距离
right_fbdate_month_gap 权利赋予日期到现在的距离
right_apply_time 权利申请持续时间
[这三个特征的统计值好像没有什么作用，有轻微反作用？]
[第一次出现也没啥作用，提升一丢丢]
```

#### 6project

```
onehot（JDDATE_Y）
DJDATE_2013, DJDATE_2014, DJDATE_2015

project_count

DJDATE_Y 第一个 表上工程 发生的年份
```

#### 7lawsuit
```
lawsuit_LAWAMOUNT_sum
lawsuit_LAWAMOUNT_count
LAWDATE_Y
```

#### 8breakfaith
```
FBDATE_Y 第一个 表上失信的年份
breakfaith_first_year 第一次失信的年份

breakfaith_is_count 总失信数
breakfaith_is_sum 已结束的失信数

SXENDDATE没怎么利用
```
#### 9recruit
```
onehot(WZCODE)
WZCODE_zp01
WZCODE_zp02
WZCODE_zp03

RECDATE_Y 第一个 表上招聘年份

recruit_count 起副作用

recruit_last_year
*recruit_last_year_to_now 

POSCODE这列数据比较脏，不知道怎么用
```

#### 可提升的地方

- branch， invest， right， lawsuit， breaksuit， recruit第一次发生的时间以及最近一次的时间？
- entbase对某些数据进行分类

# 2017/11/23
新增了一些importance程度比较高的特征

# 2017/11/24
把EID添加到特征里，到689

注册资本转换为CPI

05，27

EID前缀 p、s one-hot

qualification BEGINDATE， EXPIRYDATE的处理

空缺值处理，不要暴力fillna（-999）

recruit 数据比较脏

招聘时间（13-15年之间）和人数（X人）