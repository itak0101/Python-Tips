# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
# 日本語を含むCSVファイルを読み込み、ヘッダ行が空の部分に名前をつける
#---------------------------------------------------------------------

# ライブラリの読み込み
import pandas as pd

# CSVファイルの読み込み
df = pd.read_csv('ReadCSV_JP.csv', encoding="SHIFT-JIS")

# 処理前状態の出力
print('\n--- Before ---')
print(df.head())

# ヘッダ行が空欄の項目を書き換える(''→'ColumnN')
colnames = df.columns.values
for i, colname in enumerate(colnames):
	if 'Unnamed' in colname:
		colnames[i] = 'Column' + str(i)

# 処理後状態の出力
print('\n--- After ---')
print(df.head())

#-------------------------------------------------------------------
