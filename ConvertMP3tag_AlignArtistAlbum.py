# -* - coding: utf-8 -*-
# 同一フォルダ内に格納されているMP3のタグ情報を一致させるプログラム
# ・更新対象の MP3タグ要素は Artist, Album, AlbumArtist, OriginalArtist
# ・フォルダ内で最も多く利用されている名前で全ファイル統一する
#
# 入力例
# folder1/01 - A.mp3 (Artist: AAA)
# folder1/02 - B.mp3 (Artist: AAA)
# folder1/03 - C.mp3 (Artist: AAA)
# folder1/04 - D.mp3 (Artist: BBB)
# folder1/05 - E.mp3 (Artist: BBB)
#
# 出力例
# folder1/01 - A.mp3 (Artist: AAA)
# folder1/02 - B.mp3 (Artist: AAA)
# folder1/03 - C.mp3 (Artist: AAA)
# folder1/04 - D.mp3 (Artist: AAA)
# folder1/05 - E.mp3 (Artist: AAA)

#---------------------------------------------------------------------
# ユーザー設定値
#---------------------------------------------------------------------

# mp3格納フォルダ (最上位パスを指定)
targetFolderPath = './Convert/'

# 出力ファイル (タグ情報一覧)
logFilePath = './ConvertMP3tag_AlignArtistAlbum.txt'

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
import collections


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
def UpdateTagInfo_Align(logFilePath, updateTag):

    # ターゲットフォルダ以下にあるファイルを再起的に探索
    searchText = targetFolderPath + '/**/*.mp3'
    targetFiles = sorted(glob.glob(searchText, recursive=True))

    # ループカウンタ
    skipCount = 0

    # ターゲットファイルを一つずつ処理してゆく
    for i in range(len(targetFiles)-1):

        # ターゲットファイルのフルパス・格納ディレクトリを取得
        targetFile = os.path.abspath(targetFiles[i])
        targetDir = os.path.dirname(targetFile)

        # 処理済みフォルダ内のファイルはスキップする
        print (str(i+1) + '/' + str(len(targetFiles)) + ' ' + targetFile)

        # 処理済みフォルダ内のファイルはスキップする
        if (skipCount > 0):
            skipCount = skipCount - 1
            continue

        # ターゲットファイルと同一フォルダに格納されているファイルを探索する
        for j in range(i, len(targetFiles)):
            targetFile_2 = os.path.abspath(targetFiles[j])
            targetDir_2 = os.path.dirname(targetFile_2)
            # 格納フォルダが異なる場合はループ脱出
            if(targetDir_2 != targetDir):
                break

        # フォルダ内の最後のファイルのインデックスを設定
        lastFileIdx = j
        if(j == len(targetFiles) - 1):
            lastFileIdx = len(targetFiles)

        # フォルダ内に格納されているMP3のタグ情報を取得する(配列に格納)
        artists, albums, album_artists, original_artists = [],[],[],[]
        for k in range(i, lastFileIdx):
            targetFile_2 = os.path.abspath(targetFiles[k])
            audioInfo_2 = eyed3.load(targetFile_2)
            tag = audioInfo_2.tag
            if not tag:
                print('Info | NoTag')
                continue
            artists.append(tag.artist)
            albums.append(tag.album)
            album_artists.append(tag.album_artist)
            original_artists.append(tag.original_artist)

        # フォルダ内で最も利用されている名称を取得
        c1 = collections.Counter(artists)
        c2 = collections.Counter(albums)
        c3 = collections.Counter(album_artists)
        c4 = collections.Counter(original_artists)
        artist = c1.most_common()[0][0]
        album = c2.most_common()[0][0]
        album_artist = c3.most_common()[0][0]
        original_artist = c4.most_common()[0][0]

        # フォルダ内に格納されているMP3のタグ情報を更新する(最も利用されている値に更新)
        with open(logFilePath, mode='w', encoding='UTF-16') as f:

            # 出力ファイルのヘッダ行を出力
            f.write(',,Before,,,,After,,,' + '\r\n')
            f.write('FilePath,Diff,Artist,Album_Artist,Original_Artist,Album,Artist,Album_Artist,Original_Artist,Album' + '\r\n')

            # タグ情報の取得
            for k in range(i, lastFileIdx):
                targetFile_2 = os.path.abspath(targetFiles[k])
                audioInfo_2 = eyed3.load(targetFile_2)
                tag = audioInfo_2.tag
                if not tag:
                    print('Info | NoTag')
                    continue

                # アーティスト名・アルバム名の打ち直しによって、文字列に変化があったら Diff フラグを True にする
                diff = True
                if((tag.artist == artist) and (tag.album_artist == album_artist) and (tag.original_artist == original_artist) and (tag.album == album)):
                    diff = False

                # 出力ファイル(タグ情報)の出力
                f.write('"' + str(targetFile_2) + '"')
                f.write(',"' + str(diff) + '"')
                f.write(',"' + str(tag.artist) + '"')
                f.write(',"' + str(tag.album_artist) + '"')
                f.write(',"' + str(tag.original_artist) + '"')
                f.write(',"' + str(tag.album) + '"')
                f.write(',"' + str(artist) + '"')
                f.write(',"' + str(album_artist) + '"')
                f.write(',"' + str(original_artist) + '"')
                f.write(',"' + str(album) + '"')
                f.write('\r\n')

                # タグ情報の更新フラグがOFFの時は以降をスキップ
                if(updateTag == False):
                    continue

                # タグ情報の更新
                tag.artist = artist
                tag.album_artist = album_artist
                tag.original_artist = original_artist
                tag.album = album
                try:
                    audioInfo_2.tag.save(encoding = 'utf-16', version = tag.version, backup = False)
                except:
                    print('Exception from audioInfo.tag.save()')

        # フォルダ内のMP3は更新済のため、スキップされる様にする
        skipCount = j - i - 1


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
UpdateTagInfo_Align(logFilePath, updateMP3tag)

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
