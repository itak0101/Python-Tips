# -*- coding: utf-8 -*-
# PascalVOC形式のXMLとJPG/PNGを元に、BoundingBox付きJPG/PNGを出力する

#---------------------------------------------------------------------
# ユーザー設定値
#---------------------------------------------------------------------

# フォルダパス (ローカルPC内で PascalVoc形式データが格納されているトップフォルダ)
topFolderPath = './'

# フォルダパス (ローカルPC内で PascalVoc形式XMLが格納されているフォルダ)
xmlFolderPath = topFolderPath + '/Annotations'

# フォルダパス (ローカルPC内で 画像ファイルが格納されているフォルダ)
imgFolderPath = topFolderPath + '/JPEGImages'

# フォルダパス (ローカルPC内で処理結果を出力するフォルダ)
imgOutputPath = topFolderPath + '/AnnotatedImages'

# ファイルパス (エラーログを出力するパス)
logFilePath = topFolderPath + '/ErrorLog.txt'

# BoundingBoxの最小サイズ
minWidth = 100
minHeight = 100


#---------------------------------------------------------------------
# ライブラリの読み込み
#---------------------------------------------------------------------
import sys
import os.path
import glob
import xml.etree.ElementTree as ET
from tkinter import Tk, messagebox
from PIL import Image, ImageDraw, ImageFont

#---------------------------------------------------------------------
# メッセージボックスの表示
#---------------------------------------------------------------------
def MBox(msg):

	# Tkを定義
	root = Tk()
	root.withdraw() # Tkのrootウインドウを表示しない

	# コンソール表示
	print('\n' + msg + '\n')

	# メッセージボックスの表示
	messagebox.showerror(os.path.basename(__file__), msg)


#---------------------------------------------------------------------
# エラー終了 (コンソールとメッセージボックスでエラー内容を通知して終了)
#---------------------------------------------------------------------
def ErrorEnd(msg):

    # メッセージボックスを表示
	MBox(msg)

	# プロセス終了
	sys.exit()


#---------------------------------------------------------------------
# メイン
#---------------------------------------------------------------------
print ('--- Process Start --------------------------------')

# フォルダの存在確認 (アノテーションファイル格納フォルダ)
topFolderPath = os.path.abspath(topFolderPath)
if(os.path.exists(topFolderPath) == False):
    ErrorEnd ('Error | 指定された入力フォルダ(ルートフォルダ)が存在しません: ' + topFolderPath)

# フォルダの存在確認 (アノテーションファイル格納フォルダ)
xmlFolderPath = os.path.abspath(xmlFolderPath)
if(os.path.exists(xmlFolderPath) == False):
    ErrorEnd ('Error | 指定された入力フォルダ(XML格納フォルダ)が存在しません: ' + xmlFolderPath)

# フォルダの存在確認 (画像格納フォルダ)
imgFolderPath = os.path.abspath(imgFolderPath)
if(os.path.exists(imgFolderPath) == False):
    ErrorEnd ('Error | 指定された入力フォルダ(画像ファイル格納フォルダ)が存在しません: ' + imgFolderPath)

# フォルダの存在確認 (処理結果を出力するフォルダ)
imgOutputPath = os.path.abspath(imgOutputPath)
if(os.path.exists(imgOutputPath) == False):
    #ErrorEnd ('Error | 指定された出力先フォルダが存在しません: ' + imgOutputPath)
    os.mkdir(imgOutputPath)

# ファイル数の一致を確認 (アノテーションファイルと画像ファイル)
anoFilePaths = glob.glob(xmlFolderPath + '/*.xml')
imgFilePaths = glob.glob(imgFolderPath + '/*.jpg')
if(len(anoFilePaths) != len(imgFilePaths)):
    s = 'Error | アノテーションファイルと画像ファイルの数が一致していません'
    s = s + '\n' + str(len(anoFilePaths)) + ' Annotation Files'
    s = s + '\n' + str(len(anoFilePaths)) + ' Image Files'
    ErrorEnd (s)

# ファイルの対応を確認 (# アノテーションファイル名が AAA.xml の場合、AAA.jpgという画像があるか確認)
for i in range(len(anoFilePaths)):
    n1 = os.path.basename(anoFilePaths[i])
    n1 = os.path.splitext(n1)[0]
    for j in range(len(imgFilePaths)):
        n2 = os.path.basename(imgFilePaths[j])
        n2 = os.path.splitext(n2)[0]
        if(n1 == n2):
            b = True
            break
    else:
        ErrorEnd ('Error | アノテーションファイルに対応する画像ファイルが見つかりませんでした: ' + n1 + '.xml')

# アノテーションファイルを順に読み込んでゆく
outputLines = []
for i, anoFilePath in enumerate(anoFilePaths):

    # アノテーションファイルのパス取得
    anoFilePath = os.path.abspath(anoFilePath)
    print ( str(i) + '/' + str(len(anoFilePaths)) + ' XML: ' + anoFilePath)
    #print ( str(i) + '/' + str(len(anoFilePaths)))
    #print ( 'XML: ' + anoFilePath)

    # アノテーションファイルを開く
    anoFile = open(anoFilePath)

    # アノテーションファイル内のデータを取得 (ルート要素)
    anoRoot = (ET.parse(anoFile)).getroot()

    # アノテーションファイル内のデータを取得 (画像ファイル名)
    imgFileName = (anoRoot.find('filename')).text
    imgFilePath = imgFolderPath + '/' + imgFileName
    #print ( 'IMG: ' + imgFilePath)

    # アノテーション対象画像の読み込み
    imgInput = Image.open(imgFilePath)
    draw = ImageDraw.Draw(imgInput)

    # 画像にクラス名・アノテーション数を書き込む際のフォントを設定
    fontClass1 = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 48)
    fontClass2 = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 49)
    fontTitle1 = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 96)
    fontTitle2 = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 97)

    # アノテーションファイル内のBoundingBox情報を順に読み込んでゆく
    objectCount = 0
    for object in anoRoot.findall('object'):
        objectCount = objectCount + 1
        className = object.find('name').text
        Xmin = object.find('bndbox/xmin').text
        Ymin = object.find('bndbox/ymin').text
        Xmax = object.find('bndbox/xmax').text
        Ymax = object.find('bndbox/ymax').text
        width = int(float(Xmax) - float(Xmin))
        height = int(float(Ymax) - float(Ymin))
        #print('class: ' + className)
        #print('Xmin: ' + Xmin)
        #print('Ymin: ' + Ymin)
        #print('Xmax: ' + Xmax)
        #print('Ymax: ' + Ymax)
        #print('width: ' + str(width))
        #print('height: ' + str(height))
        #print('')

        # BoundingBoxが基準サイズ以上であることを確認
        if (width < minWidth) or (height < minHeight):
            outputLines.append(imgFilePath + ' , 基準サイズ以下の BoundingBox が見つかりました , ' + className + '(' + str(width) + '*' + str(height) + ')' )

        # BoundingBox,クラス名を描画する際の色を設定
        R = 0
        G = 0
        B = 0

        if className == 'Dog':
            R = 255
        elif className == 'Cat':
            B = 255
        else:
            outputLines.append(imgFilePath + ' , Dog,Cat以外のクラス名が見つかりました , ' + className)

        # BoudingBoxの描画
        draw.rectangle((int(float(Xmin)), int(float(Ymin)), int(float(Xmax)), int(float(Ymax))), outline=(R, G, B))

        # クラス名の描画 (視認性を高めるため、色違いの文字を重ねて袋文字にする)
        displayTxt = className + '(' + str(width) + '*' + str(height) + ')'
        draw.multiline_text(xy=(int(float(Xmin)), int(float(Ymin))-50), text=displayTxt, font=fontClass2, fill=(255, 255, 255, 0))
        draw.multiline_text(xy=(int(float(Xmin)), int(float(Ymin))-50), text=displayTxt, font=fontClass1, fill=(R, G, B, 0))

    # 合計アノテーション数の描画 (視認性を高めるため、色違いの文字を重ねて袋文字にする)
    draw.multiline_text(xy=(0, 0), text=str(objectCount) + ' Annotation(s)', font=fontTitle2, fill=(0, 0, 0, 0))
    draw.multiline_text(xy=(0, 0), text=str(objectCount) + ' Annotation(s)', font=fontTitle1, fill=(255, 255, 255, 0))

    # 編集済画像の出力 (元画像 + BoudingBox + クラス名 + 合計アノテーション数)
    imgInput = imgInput.convert('RGB')
    imgInput.save(imgOutputPath + '/' + imgFileName)

    # アノテーションファイルが切り替わるごとに、ログに1行空行が入るようにする
    #print('')

# 全ファイル終了後の処理 (終了通知とエラー出力)
if len(outputLines)==0:
    with open(logFilePath, mode='w') as f:
        pass
    MBox ('正常終了しました\n' + imgOutputPath)
else:
    try:
        with open(logFilePath, mode='w') as f:
            for line in outputLines:
                f.write(line + '\n')
    except Exception as e:
        ErrorEnd('Error | エラーログのファイル出力に失敗しました: ' + str(e))
    MBox ('処理終了しましたが、エラーが見つかりました。ログファイルを参照してください\n' + logFilePath)

print ('--- Process Finished --------------------------------\n\n')

#---------------------------------------------------------------------
# End
