import numpy as np
import matplotlib.pyplot as plt

# 定義域
beta_1 = np.linspace(-3, 5, 400)
beta_2 = np.linspace(-3, 5, 400)
B1, B2 = np.meshgrid(beta_1, beta_2)

# 残差平方和の等高線（中心をずらす）
RSS = (B1 - 2)**2 + 2*(B1 - 2)*(B2 - 1) + 3*(B2 - 1)**2

# リッジ回帰の制約（円）
ridge_constraint = B1**2 + B2**2

# プロット
plt.figure(figsize=(8, 6))
contour = plt.contour(B1, B2, RSS, levels=np.logspace(-1, 3, 20), cmap='viridis')
plt.plot(2, 1, 'ro', label='OLS Solution')  # 最小二乗法の解（楕円の中心）
plt.contour(B1, B2, ridge_constraint, levels=[1], colors='r', linewidths=2)  # リッジ回帰の制約

plt.xlabel(r'$\beta_1$', fontsize=18)
plt.ylabel(r'$\beta_2$', fontsize=18, rotation=0)
plt.title('Ridge Regression Constraint (L2 Penalty)')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
