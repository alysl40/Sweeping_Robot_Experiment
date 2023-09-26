from CW_code_rectangle import *
from Priority import *
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from openpyxl.workbook import Workbook


def runSetOfExperiments(numberOfRuns):
    dirtCollectedList = []
    for _ in range(numberOfRuns):
        dirtCollectedList.append(runOneExperiment())
    return dirtCollectedList
        
def runExperimentsWithDifferentParameters(numberOfRuns):
    resultsTable = {}                               #numberofBots从1-10
    dirtCollected = runSetOfExperiments(numberOfRuns)   
    resultsTable = dirtCollected
    results = pd.DataFrame(resultsTable)
    print(results)
    results.to_excel(excel_writer = "D:\诺丁汉大学 学习资料\诺丁汉大学  计算机科学 学习资料\Designing intelligent agent\Coursework\data_rectangle10.xlsx",sheet_name="result")
    # print(ttest_ind(results["robots: 1"],results["robots: 2"])
    print(results.mean(axis=0))
    # results.boxplot(grid=False)
    # plt.show()


runExperimentsWithDifferentParameters(50)