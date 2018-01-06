import pandas as pd

df = pd.read_csv('houseInfo.csv')

data = [house.split('|') for house in df.houseInfo]

result = []

for i in data:
    if len(i) > 6:
        result.append([i[0].strip() + ' * ' + i[1].strip()] + i[2:])
    else:
        if len(i) < 6:
            i.append('Na')
        result.append(i)

houseInfo_split = pd.DataFrame(result, index=None, columns=[
                               '小区', '户型', '面积', '朝向', '装修', '电梯'])

df = pd.merge(df, houseInfo_split, right_index=True, left_index=True)

houseType = df.groupby('户型')['户型'].agg(len)

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
houseTypeData = dict(houseType.items())
result = tuple(houseTypeData.values())
label = tuple(houseTypeData.keys())
ind = np.arange(len(houseTypeData))
height = 0.8
plt.figure(figsize=(9,8),dpi=200)
p = plt.barh(ind, result, height)
plt.xlabel('数量')
plt.ylabel('户型')
plt.title('房源分布情况')
plt.xticks(np.arange(0, 1000, 200))
plt.yticks(ind, label)
plt.legend((p, ), ('数量', ))
plt.show()
