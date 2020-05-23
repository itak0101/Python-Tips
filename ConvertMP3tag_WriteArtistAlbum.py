# -* - coding: utf-8 -*-
# フォルダ内に格納されているMP3のタグ情報を更新するプログラム
# ・更新対象の MP3タグ要素は Artist, Album, AlbumArtist, OriginalArtist, Title
# ・フォルダ内で最も多く利用されている名前で全ファイル統一する
#
# 実行例
# mp3/ArtistA/AlbumB/01 - AAA.mp3 -> 書き込まれるMP3情報 (Artist=ArtistA, AlbumArtist=ArtistA, OriginalArtist=None, Album=AlbumB, Title=AAA)
# mp3/ArtistA/AlbumB/02 - BBB.mp3 -> 書き込まれるMP3情報 (Artist=ArtistA, AlbumArtist=ArtistA, OriginalArtist=None, Album=AlbumB, Title=BBB)
# mp3/ArtistA/AlbumB/03 - CCC.mp3 -> 書き込まれるMP3情報 (Artist=ArtistA, AlbumArtist=ArtistA, OriginalArtist=None, Album=AlbumB, Title=CCC)
# mp3/ArtistA/AlbumB/04 - DDD.mp3 -> 書き込まれるMP3情報 (Artist=ArtistA, AlbumArtist=ArtistA, OriginalArtist=None, Album=AlbumB, Title=DDD)
# mp3/ArtistA/AlbumB/05 - EEE.mp3 -> 書き込まれるMP3情報 (Artist=ArtistA, AlbumArtist=ArtistA, OriginalArtist=None, Album=AlbumB, Title=EEE)

#---------------------------------------------------------------------
# ユーザー設定値
#---------------------------------------------------------------------

# mp3格納フォルダ (最上位パスを指定)
targetFolderPath = './Convert/'

# 出力ファイル (タグ情報一覧)
logFilePath = './ConvertMP3tag_WriteArtistAlbum.txt'

# タグ更新フラグ
# True:  タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新する
# False: タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新しない
updateMP3tag = False


#---------------------------------------------------------------------
# ライブラリ類の読み込み
#---------------------------------------------------------------------
import eyed3
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
    searchText = targetDir + '/**/*.mp3'
    targetFiles = sorted(glob.glob(searchText, recursive=True))
    if(len(targetFiles) == 0):
        ErrorEnd('Error | 指定されたフォルダ内に対象ファイルが存在しません ' + targetDir)


#---------------------------------------------------------------------
# ファイルのパーミション変更 (読み取り専用だった場合は書き込み可能に変更)
#---------------------------------------------------------------------
def ChangePermission_RtoW():

    # ターゲットフォルダ以下にあるファイルを再起的に探索
    searchText = targetFolderPath + '/**/*.mp3'
    targetFiles = sorted(glob.glob(searchText, recursive=True))

    # ターゲットファイルが読み取り専用の場合は、書き込み可能に変更
    for i, file in enumerate(targetFiles):
        target = os.path.abspath(file)
        if not os.access(target, os.W_OK):
            os.chmod(target, stat.S_IWRITE)


#---------------------------------------------------------------------
# 同一フォルダ内に格納されているMP3のタグ情報を一致させる (Artist, Album, AlbumArtist, OriginalArtist)
# #同一フォルダ内で最も出現回数が多い名称に統一する
#---------------------------------------------------------------------
def UpdateTagInfo_Write(logFilePath, updateTag):

    # ターゲットフォルダ以下にあるファイルを再起的に探索
    searchText = targetFolderPath + '/**/*.mp3'
    targetFiles = sorted(glob.glob(searchText, recursive=True))

    # ターゲットファイルを一つずつ処理してゆく
    with open(logFilePath, mode='w', encoding='UTF-16') as f:

        # 出力ファイルのヘッダ行を出力
        f.write(',Before,,,,,After,,,,' + '\r\n')
        f.write('FilePath,Diff,Artist,Album_Artist,Original_Artist,Title,Album,Artist,Album_Artist,Original_Artist,Album,Title' + '\r\n')

        for i, targetFile in enumerate(targetFiles):

            # 進捗情報の表示
            print (str(i+1) + '/' + str(len(targetFiles)) + ' ' + targetFile)

            # ターゲットファイルのフルパス・格納ディレクトリを取得
            targetFile = os.path.abspath(targetFile)
            targetPath = os.path.dirname(targetFile)
            targetName = os.path.splitext(os.path.basename(targetFile))[0]
            targetExt = os.path.splitext(os.path.basename(targetFile))[1]
            targetDir1 = os.path.basename(os.path.abspath(targetPath + '/../'))
            targetDir2 = os.path.basename(targetPath)

            # ファイル名からトラック番号部分を削除
            key = ' - '
            pos = targetName.rfind(key)
            if(pos != -1):
                targetName = targetName[pos + len(key):]

            # 更新後のタグ情報を設定
            artist = targetDir1
            album_artist = targetDir1
            original_artist = None
            album = targetDir2
            title = targetName

            # MP3タグ情報の取得
            audioInfo = eyed3.load(targetFile)
            tag = audioInfo.tag
            if not tag:
                print('Info | NoTag')
                continue

            # MP3情報の更新によって内容に変化があったら Diff フラグを True にする
            diff = True
            if((tag.artist == artist) and (tag.album_artist == album_artist) and (tag.original_artist == original_artist) and (tag.album == album) and (tag.title == title)):
                diff = False

            # 出力ファイル(タグ情報)の出力
            f.write('"' + str(targetFile) + '"')
            f.write(',"' + str(diff) + '"')
            f.write(',"' + str(tag.artist) + '"')
            f.write(',"' + str(tag.album_artist) + '"')
            f.write(',"' + str(tag.original_artist) + '"')
            f.write(',"' + str(tag.album) + '"')
            f.write(',"' + str(tag.title) + '"')
            f.write(',"' + str(artist) + '"')
            f.write(',"' + str(album_artist) + '"')
            f.write(',"' + str(original_artist) + '"')
            f.write(',"' + str(album) + '"')
            f.write(',"' + str(title) + '"')
            f.write('\r\n')

            # タグ情報の更新フラグがOFFの時は以降をスキップ
            if(updateTag == False):
                continue

            # タグ情報の更新
            tag.artist = artist
            tag.album_artist = album_artist
            tag.original_artist = original_artist
            tag.album = album
            tag.title = title
            try:
                audioInfo.tag.save(encoding = 'utf-16', version = (2, 4, 0), backup = False)
            except:
                print('Exception from audioInfo.tag.save()')


#---------------------------------------------------------------------
# メイン
#---------------------------------------------------------------------

print('■ Process Start')

# 設定値の妥当性チェック
CheckParams()

# ファイルのパーミション変更 (読み取り専用だった場合は書き込み可能に変更)
ChangePermission_RtoW()

#同一フォルダ内に格納されているMP3のタグ情報を一致させる (Artist, Album, AlbumArtist, OriginalArtist)
#同一フォルダ内で最も出現回数が多い名称に統一する
# updateTag=True:  タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新する
# updateTag=False: タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新しない
UpdateTagInfo_Write(logFilePath, updateMP3tag)

print('■ Process Finished')


#---------------------------------------------------------------------
# 参考資料
#---------------------------------------------------------------------
# [1] Mac における MP3 ファイルの文字化けを直してみた
# https://abicky.net/2013/01/23/072137/
#
# [2] eyed3 / mp3のtag情報をpythonで操作する
# https://qiita.com/harasakih/items/313ecde24e3239f71ae7
#
# [3] Docs » eyed3 module » eyed3 package » eyed3.id3 package
# https://eyed3.readthedocs.io/en/latest/eyed3.id3.html#module-eyed3.id3.tag
#
# [4] Shift_JISとUTF-8とASCIIを行き来する
# https://qiita.com/inoory/items/aafe79384dbfcc0802cf
#
# [5] Pythonのchardetで文字コード判定
# https://blog.imind.jp/entry/2019/08/24/143939
#
#---------------------------------------------------------------------
# End
