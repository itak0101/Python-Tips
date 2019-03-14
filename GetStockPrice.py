# -*- coding: utf-8 -*-

#---------------------------------------------------------------------
# ライブラリ類の読み込み
#---------------------------------------------------------------------
import os
import lxml.html
import requests
from datetime import datetime
import schedule
import time
import csv

#---------------------------------------------------------------------
# 指定された銘柄の株価を取得する (Google検索を利用)
#---------------------------------------------------------------------
def GetCurrentPrice(sBrandName):
	
	# Google検索を実行して検索結果のHTMLを取得する
	sURL = 'https://www.google.co.jp/search?q=' + sBrandName + '株価&ie=UTF-8'
	sHTML = requests.get(sURL).text
	#with open('Debug.html', mode='w') as f:
	#	f.write(sHTML)
	
	# 抽出開始と抽出終了の位置を文字で設定
	nStart = int(sHTML.find('<span style="font-size:157%"'))     # 開始位置
	nEnd = int(sHTML.find('&nbsp;<cite style="color:#cc0000">')) # 終了位置
	#print('from ' + str(nStart) + ' to ' + str(nEnd))
	
	# 抽出
	sPrice = sHTML[nStart:nEnd]
	#print(sPrice)
	
	# 抽出結果から更に抽出(最初の<br>から先を取得)
	sPrice = sPrice[int(sPrice.find('<b>'))+3:]
	#print(sPrice)
	
	# 抽出結果から更に抽出(最初の</br>までを取得)
	sPrice = sPrice[:int(sPrice.find('</b>'))]
	#print(sPrice)
	
	# 桁区切りのカンマを削除
	sPrice = sPrice.replace(',', '')
	#print(sPrice)
	
	# 現在時刻を取得
	sTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	outdata = '"' + sBrandName + '","' + sTime + '","' + sPrice + '"'
	print(outdata)
	
	# ファイル出力(ファイルが存在していなければ作成&ヘッダ出力する。その後は追記)
	sCurrentDir = os.path.dirname(os.path.abspath(__file__))
	sOutputPath = sCurrentDir + '\GetStockPrice_' + sBrandName + '.csv'
	if not os.path.exists(sOutputPath):
		with open(sOutputPath, mode='a') as f:
			f.write("Name,Time,Price\n")
	with open(sOutputPath, mode='a') as f:
		f.write(outdata + "\n")
		
	# 取得結果を配列形式にして戻り値とする
	return [sBrandName, sTime, sPrice]


#---------------------------------------------------------------------
# 定期実行処理
#---------------------------------------------------------------------
# 株価取得 (コンソール出力 + CSVファイル出力)
def ScheduledJob():
	
	# 株価取得 (コンソール出力 + CSVファイル出力)
	dataList = GetCurrentPrice("楽天")


#---------------------------------------------------------------------
# メイン処理
#---------------------------------------------------------------------

# コンソールに案内情報を表示
print("10分おきに現在株価を表示します\n")

# 開始時にScheduledJobを一度実行
ScheduledJob()

# 以降は10分毎にScheduledJobを実行
schedule.every(10).minutes.do(ScheduledJob)

# 現在時刻がScheduledJobを実行するタイミングか否かは10秒ごとに判定する
while True:
    schedule.run_pending()
    time.sleep(10)


#---------------------------------------------------------------------

