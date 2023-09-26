# The flowing code is written by myself


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
from scipy import stats
from statsmodels.graphics.gofplots import qqplot

df = pd.read_excel("D:\诺丁汉大学 学习资料\诺丁汉大学  计算机科学 学习资料\Designing intelligent agent\Coursework\data.xlsx")

plt.plot(df['Experiment number'],df['Square'],color = 'blue',label = 'Square')
plt.plot(df['Experiment number'],df['Triangle'], color = 'red',label = 'Triangle')
plt.plot(df['Experiment number'],df['Rectangle'],color = 'green', label = 'Rectangle')

plt.title('Experimental data line chart')
plt.xlabel('Experiment number')
plt.ylabel('Dust Collection Quantity')
plt.legend()
plt.show()

plt.boxplot([df['Square'],df['Triangle'],df['Rectangle']])
plt.title('Experimental data line chart')
plt.xticks([1,2,3],['Square','Triangle','Rectangle'])
plt.ylabel('Dust Collection Quantity')
plt.show()

header = ['Square','Triangle','Rectangle']

# Mean
mean_result = []
Median_result = []
Mode_result = []
Variance_result = []
Stdev_result = []

for h in header:
    mean = statistics.mean(df[h])
    Median = statistics.median(df[h])
    Mode = statistics.mode(df[h])
    Variance = statistics.variance(df[h])
    Stdev = statistics.stdev(df[h])
    
    mean_result.append(mean)
    Median_result.append(Median)
    Mode_result.append(Mode)
    Variance_result.append(Variance)
    Stdev_result.append(Stdev)

result_df = pd.DataFrame()
result_df[''] = header
result_df['Mean'] = mean_result
result_df['Median'] = Median_result
result_df['Mode'] = Mode_result
result_df['Variance'] = Variance_result
result_df['Stdev'] = Stdev_result
result_df.to_excel(excel_writer='D:\诺丁汉大学 学习资料\诺丁汉大学  计算机科学 学习资料\Designing intelligent agent\Coursework\Result.xlsx',sheet_name='Result')

#normal distribution
qqplot(df['Rectangle'],line = 's')
plt.show()








#Welch's t-test
for h in header:
    for i in header:
        if h != i:
            t_statistic,p = stats.ttest_ind(df[h],df[i],equal_var=False) 
            print(str(h)+" "+str(i)+" p value is: "+str(p))
    print('\n')
        

