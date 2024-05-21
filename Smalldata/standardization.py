import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 2次元のガウス分布を作る

x = np.random.multivariate_normal([4, 5], [[2.0, 1.0], [1.0, 4.0]], 50 )

# xをplotする。
# x軸とy軸も描画する。
plt.figure(figsize=(6, 6))
plt.grid(True)

plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.plot(x[:, 0], x[:, 1], '.')
plt.show()

# xを標準化する。
std_x = StandardScaler().fit_transform(x)

# 標準化したxをplotする。
plt.figure(figsize=(6, 6))
plt.grid(True)

plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.plot(x[:, 0], x[:, 1], '.')
plt.plot(std_x[:, 0], std_x[:, 1], '.', color='red')
plt.show()

