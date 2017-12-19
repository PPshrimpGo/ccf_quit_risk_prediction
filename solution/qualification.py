from utils import *
import pandas as pd
import numpy as np

def is_over(x):
    try:
        if x >= 2017:
            return 1
        else:
            return 0
    except:
        return 0

def qualification():
    qualification = pd.read_csv("../public/10qualification.csv", encoding="gbk")
    output = pd.DataFrame()
    output["EID"] = qualification.groupby("EID").count().index

    qualification_count = qualification.groupby("EID", as_index=False)["ADDTYPE"].count()
    qualification_count.rename(columns={"ADDTYPE": "qualification_count"}, inplace=True)
    output = pd.merge(output, qualification_count, on=["EID"], how="left")

    return output

if __name__ == "__main__":
    qualification()
