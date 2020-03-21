# -*- coding: utf-8 -*-
# 入力フォルダに格納されている XLSファイルを出力フォルダにコピーする
# コピーの際に、XLSファイルの最左セルのA1セルに入力されている文字列をXLSファイル名に付与する。

#---------------------------------------------------------------------
# ユーザー設定値
#---------------------------------------------------------------------

# トップフォルダ
topFolderPath = './'

# 入力ファイル格納フォルダ
inputFolderPath = 'Input'

# 出力ファイル格納フォルダ (存在しなければ自動生成される)
outputFolderPath = 'Output'


#---------------------------------------------------------------------
# ライブラリ類の読み込み
#---------------------------------------------------------------------
import os
import glob
import xlrd  # ExcelRead (xls,xlsx)
import shutil
import sys


#---------------------------------------------------------------------
# メイン
#---------------------------------------------------------------------

# フォルダの存在確認 (トップフォルダ)
topFolderPath = os.path.abspath(topFolderPath)
if(os.path.exists(topFolderPath) == False):
    print ('Error | 指定されたフォルダ(トップフォルダ)が存在しません: ' + topFolderPath)
    sys.exit()

# フォルダの存在確認 (入力ファイル格納フォルダ)
inputFolderPath = os.path.abspath(inputFolderPath)
if(os.path.exists(inputFolderPath) == False):
    print ('Error | 指定されたフォルダ(入力データ格納フォルダ)が存在しません: ' + inputFolderPath)
    sys.exit()

# フォルダの存在確認 (出力ファイル格納フォルダが存在していたら削除してから新規作成、存在していなければ新規作成)
outputFolderPath = os.path.abspath(outputFolderPath)
if(os.path.exists(outputFolderPath) == True):
    shutil.rmtree(outputFolderPath)
os.mkdir(outputFolderPath)

# 入力ファイル格納フォルダ内のXLSファイルのパス一覧を取得する
xlsFilePaths = glob.glob(inputFolderPath + '/*.xls')
if(len(xlsFilePaths) == 0):
    print ('Error | 入力ファイル格納フォルダにXLSファイルが格納されていません: ' + inputFolderPath)
    sys.exit()

# パス一覧をもとに、1つずつXLSファイルを当たってゆく
for i, xlsFilePath in enumerate(xlsFilePaths):

    # XLSファイルのパス取得
    xlsFilePath = os.path.abspath(xlsFilePath)
    print ( str(i+1) + '/' + str(len(xlsFilePaths)) + ' Excel: ' + xlsFilePath)

    # XLSファイルのファイル名(拡張子なし)を取得
    filename = os.path.basename(xlsFilePath)  # フルパスからファイル名(拡張子あり)を取得 (aaa/bbb/ccc.xlsx → ccc.xlsx)
    filename = os.path.splitext(filename)[0]  # ファイル名(拡張子なし)を取得 (ccc.xlsx → ccc)

    # XLSファイルを開き、最左のシートの、A1セルの文字列を取得する
    book = xlrd.open_workbook(xlsFilePath)
    sheet = book.sheet_by_index(0)        # シートを取得(シート番号で指定)
    #sheet = book.sheet_by_name('名簿２')  # シートを取得(シート名で指定)
    cell = sheet.cell(0, 0)               # セルを取得(A1セルは x=0, y=0)
    value = str(cell.value)               # セルに記載されている値を取得

    # XLSファイルをクローズする (これをしないとメモリ使用量が際限なく増えていってしまうはず)
    book.release_resources()
    del book

    # XLSファイルをコピーする (入力ファイル格納フォルダ -> 出力ファイル格納フォルダ)、ついでにA1セルの文字列をファイル名に付与する)
    shutil.copy2(xlsFilePath, outputFolderPath + '/' + filename + '_' + value +  '.xls')

    # テキストファイルを出力する (Excelファイル名とそのA1セルの値を記載)
    with open(outputFolderPath + '/AggregateExcel.txt', mode='a') as f:
        f.write(xlsFilePath + ',' + value + '\r\n')

#---------------------------------------------------------------------
# End
