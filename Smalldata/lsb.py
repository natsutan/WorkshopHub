import numpy as np
import matplotlib.pyplot as plt

# データの生成
np.random.seed(0)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# 行列を使った最小二乗法
X_b = np.c_[np.ones((100, 1)), X]  # X0 = 1 を追加
theta_best = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y

# 回帰直線の計算
X_new = np.array([[0], [2]])
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b @ theta_best

# プロット
plt.plot(X_new, y_predict, "r-", linewidth=2, label="Predictions")
plt.plot(X, y, "b.", label="Data")
plt.xlabel("$x_1$", fontsize=18)
plt.ylabel("$y$", fontsize=18, rotation=0)
plt.legend(loc="upper left")
plt.title("Linear Regression using Least Squares")
plt.axis([0, 2, 0, 15])
plt.grid(True)
plt.show()
