import numpy as np
import matplotlib.pyplot as plt

np.random.seed(3)
# 平均0、分散が2.0のガウス分布のグラフを書く
# サンプルベースでは無く数式で綺麗なグラフを書く

# ガウス分布の確率密度関数
def gaussian(x, mu, sigma):
    return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / np.sqrt(2 * np.pi * sigma ** 2)

x = np.linspace(-10, 10, 100)
y = gaussian(x, 0, 2.0)

# mu=0, sigma=2.0をグラフに文字で書く
plt.text(-9, 0.1, r'$\mu=0, \sigma=2.0$')

plt.plot(x, y)
plt.show()

# 平均0、分散が2.0のガウス分布の確率分布を作る。
# サンプリングできるようにする
def gaussian_sampling(mu, sigma, n):
    return np.random.normal(mu, sigma, n)

# 10回、20回、100回とサンプリングし、分散と標本分散をそれぞれ計算する。
for n in [10, 20, 100]:
    x = gaussian_sampling(0, 2.0, n)
    print(f'n={n}, variance={np.var(x, ddof=0)}, sample variance={np.var(x, ddof=1)}')


