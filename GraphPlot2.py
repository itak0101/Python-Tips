# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# データ設定

# 関数型
x = np.arange(-np.pi, np.pi, np.pi/100) 
plt.plot(x, np.sin(x)*10)
plt.plot(x, np.cos(x)*20)

# 散布図型
plt.plot([-1,0,1],[10,0,-10])
plt.plot([-1,0,1],[20,0,-20])

# ヒストグラム型
x2 = np.random.randn(1000)
plt.hist(x2-0.5, bins=10, alpha=0.3, histtype='stepfilled', color='r')

# グラフ表示設定
plt.title('Title')
plt.xlabel('Y')
plt.ylabel('X')
plt.legend(['Graph1','Graph2','Graph3','Graph4','Graph5'])
plt.grid(True)

# グラフ表示実行
plt.savefig('GraphPlot.png')

# グラフの画面表示
plt.show()

#---------------------------------------------------------------------
# End
