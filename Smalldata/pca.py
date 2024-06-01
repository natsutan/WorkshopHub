# ここからデータをダウンローし、csvへ変換する。
# ファイル名をgrade.csvとして、utf-8で保存する。
# https://estat.sci.kagoshima-u.ac.jp/data/cgi-bin/data/whats_data/data/img/932722923_9821.xls

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# データをutf-8で読み込む
data = np.loadtxt('grade.csv', delimiter=',', skiprows=1, usecols=[1, 2, 3, 4, 5],  encoding="utf-8")

# データを標準化する。
std_data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

# 主成分分析を行う
pca = PCA()
pca.fit(std_data)

# 主成分分析の結果をplotする。
plt.figure(figsize=(6, 6))
plt.grid(True)

# 主成分分析の結果と主軸をplotする。
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.plot(std_data[:, 0], std_data[:, 1], '.')


plt.show()


# 第一主成分と第二主成分でプロットする
plt.figure(figsize=(6, 6))

for x, y, name in zip(pca.components_[0], pca.components_[1], ['Japanese', 'English', 'Math', 'Physics', 'chemistry']):
    plt.text(x, y, name)
plt.scatter(pca.components_[0], pca.components_[1], alpha=0.8)

plt.grid()
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()



