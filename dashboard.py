# 航空乘客满意度数据分析与可视化
# 本分析基于airline_passenger_satisfaction.csv数据，展示各满意度指标分布及自变量与满意度（Satisfaction）之间的相关性。代码可直接部署于Streamlit。

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置为黑体或其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False    # 正确显示负号

# 读取数据
df = pd.read_csv(r'c:/Users/YY/Desktop/dashboard_v2/airline_passenger_satisfaction.csv')
st.title('航空乘客满意度数据分析')
st.write('数据总量：', df.shape[0])
st.write('字段：', list(df.columns))

# 1. 满意度分布情况
fig1, ax1 = plt.subplots()
sns.countplot(x='Satisfaction', data=df, ax=ax1)
ax1.set_title('满意度分布')
st.pyplot(fig1)

# 2. 各满意度指标分布
metrics = ['Departure and Arrival Time Convenience','Ease of Online Booking','Check-in Service','Online Boarding','Gate Location','On-board Service','Seat Comfort','Leg Room Service','Cleanliness','Food and Drink','In-flight Service','In-flight Wifi Service','In-flight Entertainment','Baggage Handling']
for metric in metrics:
    fig, ax = plt.subplots()
    sns.histplot(df[metric], bins=6, kde=False, ax=ax)
    ax.set_title(f'{metric} 分布')
    st.pyplot(fig)

# 3. 各自变量与满意度的相关性分析
corr_metrics = metrics + ['Age','Flight Distance','Departure Delay','Arrival Delay']
df_corr = df.copy()
df_corr['Satisfaction_num'] = df_corr['Satisfaction'].map({'Satisfied':1, 'Neutral or Dissatisfied':0})
corrs = df_corr[corr_metrics + ['Satisfaction_num']].corr()['Satisfaction_num'].sort_values(ascending=False)
st.write('各指标与满意度相关性：')
st.write(corrs)
fig2, ax2 = plt.subplots(figsize=(8,10))
sns.heatmap(df_corr[corr_metrics + ['Satisfaction_num']].corr(), annot=True, cmap='coolwarm', ax=ax2)
ax2.set_title('相关性热力图')
st.pyplot(fig2)

# 4. 结论与建议
# 满意度分布可见大部分乘客为满意或中立/不满意。
# 各服务指标与满意度相关性不同，可据此优化服务重点。
# 可进一步细分分析不同客户类型、舱位等对满意度的影响。