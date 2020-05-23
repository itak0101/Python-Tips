# -* - coding: utf-8 -*-
# MP3ファイルのファイル名を整えるプログラム
# ・MP3ファイルの拡張子が「.MP3」の場合「.mp3」に書き換え
# ・MP3ファイル名の全角スペースを半角スペースに変更
# ・MP3ファイル名の先頭2文字が '- ' の場合は当該部分を削除

#---------------------------------------------------------------------
# ユーザー設定値
#---------------------------------------------------------------------

# mp3格納フォルダ (最上位パスを指定)
targetFolderPath = './Convert/'

# 出力ファイル (タグ情報一覧)
logFilePath = './ConvertMP3tag_Rename.txt'

# ファイル名 更新フラグ
# True:  タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新する
# False: タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新しない
updateName = False


#---------------------------------------------------------------------
# ライブラリ類の読み込み
#---------------------------------------------------------------------
import glob
import sys
import os
from tkinter import Tk, messagebox


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
# 設定値の妥当性確認
#---------------------------------------------------------------------
def CheckParams():

    # ターゲットフォルダパス(設定値)を絶対パスに変換
    targetDir = os.path.abspath(targetFolderPath)

    # 設定値のチェック (入力フォルダパスがフォルダパスであるか。ファイルパスで無いか)
    if (os.path.isdir(targetDir) == False):
        ErrorEnd('Error | 指定されたパスはフォルダパスではありません ' + targetDir)

    # 設定値のチェック (入力されたフォルダパスが実在するか)
    if (os.path.exists(targetDir) == False):
        ErrorEnd('Error | 指定されたフォルダが存在しません ' + targetDir)

    # ターゲットフォルダ以下にあるファイルを再起的に探索
    searchText = targetDir + '/**/*.*3'
    targetFiles = sorted(glob.glob(searchText, recursive=True))
    if(len(targetFiles) == 0):
        ErrorEnd('Error | 指定されたフォルダ内に対象ファイルが存在しません ' + targetDir)


#---------------------------------------------------------------------
# ファイル名を変更
#---------------------------------------------------------------------
def ChangeFileName(logFilePath, updateName):

    # ターゲットフォルダ以下にあるファイルを再起的に探索
    searchText = targetFolderPath + '/**/*.*3'
    targetFiles = sorted(glob.glob(searchText, recursive=True))

    # ターゲットファイルが読み取り専用の場合は、書き込み可能に変更
    with open(logFilePath, mode='w') as f:

        # 出力ファイルのヘッダ行を出力
        f.write('Diff,FileName(Before),FileName(After)' + '\r\n')

        # 出力ファイルのヘッダ行を出力
        for i, file in enumerate(targetFiles):

            # 変更前ファイル名を取得
            target = os.path.abspath(file)

            # 変更後ファイル名を設定
            target_2 = os.path.basename(target)         # ファイル名部分のみ取得
            target_2 = target_2.replace('.MP3', '.mp3') # 大文字拡張子を小文字拡張子に変換
            target_2 = target_2.replace('　', ' ')      # 全角スペースを半角スペースに変更
            if(target_2[:2]=='- '):                     # 先頭2文字が '- ' の場合は削除
                target_2 = target_2[2:]
            target_2 = os.path.dirname(target) + '/' + target_2

            # リネーム実行
            diff = True
            if ('.mp3' not in target_2) or (target == target_2):
                diff = False
            f.write(str(diff) + ',' + target + ',' + target_2 + '\r\n')
            print(str(i+1) + '/' + str(len(targetFiles)) + ' Rename: from ' + target + ' to ' + target_2)

            # リネーム実行
            if((updateName == True) and (diff == True)):
                os.rename(target, target_2)


#---------------------------------------------------------------------
# メイン
#---------------------------------------------------------------------

print('■ Process Start')

# 設定値の妥当性チェック
CheckParams()

# ファイル名を変更
ChangeFileName(logFilePath, updateName)

print('■ Process Finished')


#---------------------------------------------------------------------
# End
