# 航空公司客户满意度分析数据说明  
# 该数据集包含来自 120,000 多名航空公司乘客的客户满意度评分信息，包括每位乘客、其航班和旅行类型的附加信息，以及对清洁度、舒适度、服务和整体体验等不同因素的评价。

# 1、第三方数据库导入及读取数据
#有任何需要的第三方库记得提前导入
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#读取数据
df = pd.read_csv("airline_passenger_satisfaction.csv")


# 2、数据预览与预处理
#查看数据前几行
df.head()
#查看数据维度
df.shape
#查看详细信息
df.info()
# 删除缺失值
df.dropna(axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)
#了解数据分布情况
df.describe()

# 3、探索性数据分析
# 任务1：该航空公司的整体满意度水平如何？在 `对机上 WiFi 服务的满意度水平` 的评价中，有多少人给了5分？
# 该航空公司的整体满意度水平如何?
print(df["Satisfaction"].value_counts())
satisfaction_rate = round(len(df[df['Satisfaction']=='Satisfied'])/len(df['Satisfaction']),2)
print(satisfaction_rate)
# 航司满意度反馈为‘满意’的占比为43%，其余全部认为‘中立’或‘不满意’。可见航司满意度水平在绝对值角度上来说较低。

# 在对机上 WiFi 服务的满意度水平 的评价中，有多少人给了5分？
five_stars = len(df[df['In-flight Wifi Service']==5])
print(five_stars)
# 在对机上 WiFi 服务的满意度水平 的评价中，有14304人给了5分。


# 任务2：该航空公司的14个分项目评分中，最差的是那个项目？  
# 可以使用平均值作为评估指标，也可以考虑其他更合适的指标，只要合理即可
score = df.iloc[:,9:23].mean()
min_avg_score = score.min()
min_avg_score_column_name = score[score == min_avg_score].index[0]
print(score.sort_values())
print(f"评分最低的项目是：{min_avg_score_column_name}")


# 任务3：该航空公司起飞延误、到达延误的情况如何？  
# 可以使用中位数作为评估指标，也可以考虑其他更合适的指标，只要合理即可
# 起飞延误中位数、到达延误中位数
depart_median = df['Departure Delay'].median()
arr_median = df['Arrival Delay'].median()
print(depart_median)
print(arr_median)
print('从中位数来看，该航司的起飞延误和到达延误中位数均为0，可以视为延误较少')
# 平均起飞延误时间：所有起飞延误航班的延误时间总和除以起飞延误航班数量。反映了航班起飞延误的平均程度。例如，100 个起飞延误航班的延误时间总和为 500 分钟，那么平均起飞延误时间为 5 分钟。
# 平均到达延误时间：所有到达延误航班的延误时间总和除以到达延误航班数量。体现了航班到达延误的平均水平。
depart_avg = df['Departure Delay'].mean()
arr_avg = df['Arrival Delay'].mean()
print(depart_avg)
print(arr_avg)
print('从平均数来看，该航司的起飞延误和到达延误的平均值分别为14.64和15.09，基本相等，平均延误时长较低')
# 最长起飞延误时间：在一定时间段内，所有航班中起飞延误时间最长的值。可以反映出极端情况下的延误情况。
# 最长到达延误时间：同理，是一定时间段内到达延误时间最长的值。
depart_max = df['Departure Delay'].max()
arr_max = df['Arrival Delay'].max()
print(depart_max)
print(arr_max)
print('从最长延误时间来看，该航司的最长起飞延误和到达延误时间分别为1592和1584.0，基本相等，表明存在极端延误的情况')
# 起飞延误率：起飞延误航班数量占总航班数量的比例。计算公式为：起飞延误率 = 起飞延误航班数 ÷ 总航班数 ×100%。例如，一个月内共有 1000 个航班，其中有 200 个航班出现起飞延误，那么起飞延误率为 20%。
# 到达延误率：到达延误航班数量占总航班数量的比例。计算方法与起飞延误率类似。
depart_rate = len(df[df['Departure Delay']>0])/len(df['Departure Delay'])
arr_rate = len(df[df['Arrival Delay']>0])/len(df['Arrival Delay'])
print(depart_rate)
print(arr_rate)
print('延误率来看，该航司的起飞和到达延误率分别为43.46%和43.81%，基本相等，延误率都处于较高水平')
# 准点率：准点航班数量占总航班数量的比例。准点航班通常定义为起飞延误时间在一定范围内（如 15 分钟以内）的航班。准点率 = 准点航班数 ÷ 总航班数 ×100%。与延误率相反，准点率越高说明航班运行越正常。
punctuality_rate = len(df[(df['Departure Delay']>15)|(df['Arrival Delay']>15)])/len(df)
print(punctuality_rate)
print('从准点率来看，该航司的准点率为26.86%，准点率较低')


# 任务4：该航空公司最受那个年龄段人群的喜爱？
age_counts = df[df['Satisfaction']=='Satisfied']['Age'].value_counts()
max_satisfaction_age = age_counts.idxmax()
print("满意度最高的人数的年龄是:", max_satisfaction_age)

#把表示满意的人的数据根据年龄聚合，并计算每个年龄群体中觉得满意的人数的占比
total_per_age = df.groupby('Age')['Satisfaction'].count()
age_counts = df[df['Satisfaction'] == 'Satisfied'].groupby('Age')['Satisfaction'].count()
age_percent = age_counts/total_per_age
plt.figure(figsize=(18,6))
sns.barplot(x=age_percent.index, y=age_percent.values)
plt.title('Age Group with the Highest Satisfaction')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()
# 满意度最高的年龄为39岁，满意度较高的人群集中在39-60岁，22-38岁的年轻群体满意度较低，建议调研年轻群体满意度低的原因

# 任务5：分析 `航班目的（商务/个人）` 与 `乘客座位所在的飞机旅行舱级别` 之间的关系
class_travel = df.groupby([ 'Type of Travel','Class'])['Class'].count().reset_index(name='amount')
print(class_travel)
plt.figure(figsize=(10,6))
ax = sns.barplot(x='Class', y='amount', hue='Type of Travel', data=class_travel)
plt.title('Relationship between Flight Purpose and Travel Class')
plt.xlabel('Class')
plt.ylabel('amount')
plt.show()
# 总结：乘坐商务舱的乘客大部分为商务出行，乘坐经济舱的乘客更多为个人出行，乘坐超级经济舱的乘客中商务和个人出行各占一半。可以把商务舱相关推荐给商务出行的个人或公司。


# 分析小结  
# 1、在整体满意度方面，航司满意度反馈为‘满意’的占比为43%，其余全部认为‘中立’或‘不满意’。可见航司满意度水平在绝对值角度上来说较低。其中，在对机上 WiFi 服务的满意度水平 的评价中，有14304人给了5分。  
# 2、在起飞延误和到达延误方面，从中位数来看，该航司的起飞延误和到达延误中位数均为0，可以视为延误较少；从平均数来看，该航司的起飞延误和到达延误的平均值分别为14.64和15.09，基本相等，平均延误时长较低；从最长延误时间来看，该航司的最长起飞延误和到达延误时间分别为1592和1584.0，基本相等，表明存在极端延误的情况；延误率来看，该航司的起飞和到达延误率分别为43.46%和43.81%，基本相等，延误率都处于较高水平；从准点率来看，该航司的准点率为26.86%，准点率较低。  
# 3、在满意度分布方面，满意度最高的年龄为39岁，满意度较高的人群集中在39-60岁，22-38岁的年轻群体满意度较低，建议调研年轻群体满意度低的原因。  
# 4、在航班目的和乘客座位所在的飞机旅行舱级别之间的关系方面，乘坐乘坐商务舱的乘客大部分为商务出行，乘坐经济舱的乘客更多为个人出行，乘坐超级经济舱的乘客中商务和个人出行各占一半。可以把商务舱相关推荐给商务出行的个人或公司。  
