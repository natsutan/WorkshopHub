import numpy as np
import matplotlib.pyplot as plt


# seedの固定
np.random.seed(0)

# 2次元のガウス分布を作る

x = np.random.multivariate_normal([4, 5], [[1.8, 0.8], [0.8, 4.0]], 50 )

# xをplotする。
# x軸とy軸も描画する。
plt.figure(figsize=(6, 6))
plt.grid(True)

plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.plot(x[:, 0], x[:, 1], '.')
plt.show()

# xを標準化する。
std_x = (x - np.mean(x, axis=0)) / np.std(x, axis=0)

# 標準化したxをplotする。
plt.figure(figsize=(6, 6))
plt.grid(True)

# 1σ、2σ、3σの円を描画する。色はRGB=0x6f723f
circle1 = plt.Circle((0, 0), 1, color='#6f723f', fill=False)
circle2 = plt.Circle((0, 0), 2, color='#6f723f', fill=False)
circle3 = plt.Circle((0, 0), 3, color='#6f723f', fill=False)

plt.gca().add_artist(circle1)
plt.gca().add_artist(circle2)
plt.gca().add_artist(circle3)

plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.plot(x[:, 0], x[:, 1], '.')
plt.plot(std_x[:, 0], std_x[:, 1], '.', color='red')
plt.show()

