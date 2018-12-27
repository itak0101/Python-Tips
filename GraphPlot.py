# -*- coding: utf-8 -*-

#---------------------------------------------------------------------
# ライブラリの読み込み
#---------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


#---------------------------------------------------------------------
# 横棒グラフの表示
#---------------------------------------------------------------------
def PlotBarGraph():

	# 擬似データ作成
	values = [3, 12, 5, 18, 45]
	series = ('A', 'B', 'C', 'D', 'E')
	y_pos = np.arange(len(series)) # 通番を格納した配列を作成 [0,1,2,...,len(series)]
	
	# グラフタイトルの設定
	plt.title("TITLE")
	
	# 横軸の設定(値)
	plt.barh(y_pos, values)
	plt.xlabel('X')
	 
	# 縦軸の設定(系列名)
	plt.yticks(y_pos, series)
	plt.ylabel('Y')
	
	# グラフを表示する
	plt.show()


#---------------------------------------------------------------------
# Entry Point
#---------------------------------------------------------------------

# CSVデータの読み込み(統計データ)
df = pd.read_csv('StatData.csv', sep=',')
#print(df.head())

# グラフのスタイル設定 (Gnuplot & Meiryo)
plt.style.use('ggplot') 
font = {'family' : 'Miryo UI'}
mpl.rc('font', **font)
df.plot(y=['Male', 'Female', 'Total'], alpha=0.5)

# グラフのラベル設定
plt.title("Town")
plt.ylabel('Population')
plt.xlabel('Survey Time')

# グラフの表示
plt.show()

#---------------------------------------------------------------------
# Reference
#---------------------------------------------------------------------
#
# [01] pyplot — Matplotlib 2.0.2 documentation
# https://matplotlib.org/api/pyplot_api.html
#
# [02] Numpy developer guide
# https://docs.scipy.org/doc/numpy/dev/
# 
# [03] matplotlib入門 / りんごがでている
# http://bicycle1885.hatenablog.com/entry/2014/02/14/023734
#
# [02] Horizontal barplot / The Python Graph Gallary
# https://python-graph-gallery.com/2-horizontal-barplot/
#
#
#---------------------------------------------------------------------
# Memo
#---------------------------------------------------------------------
#
#