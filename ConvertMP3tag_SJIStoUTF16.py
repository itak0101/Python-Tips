# -* - coding: utf-8 -*-
# MP3ファイルのタグ情報が SJIS で書き込まれている場合、UTF-16に書き換えるプログラム
# ・古いMP3ファイルはタグ情報が SJIS で書き込まれている場合がある。
# ・現在はMP3ファイルのタグ情報は UTF-16 で書き込むルールになっている。
# ・よって最近の音楽プレーヤー等で古いMP3ファイルを読み込んだ際に SJIS の日本語が文字化けする。
# ・SJISで書き込まれたタグ情報をUTF-16に変換するのが本プログラムである。
# ・更新対象の MP3タグ要素は Artist, Album, AlbumArtist, OriginalArtist, disc_num, track_num, title

#---------------------------------------------------------------------
# ユーザー設定値
#---------------------------------------------------------------------

# mp3格納フォルダ (最上位パスを指定)
targetFolderPath = './Convert/'

# 出力ファイル (タグ情報一覧)
logFilePath = './ConvertMP3tag_SJIStoUTF16.txt'

# タグ更新フラグ
# True:  タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新する
# False: タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新しない
convertMP3tag = False


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
# タグ情報を一覧出力する + タグ情報を更新する
#---------------------------------------------------------------------
def ConvertTagInfo_SJIStoUTF16(encodeInfoFilePath, updateTag):

    # ターゲットフォルダ以下にあるファイルを再起的に探索
    searchText = targetFolderPath + '/**/*.mp3'
    targetFiles = sorted(glob.glob(searchText, recursive=True))

    # 出力ファイル(タグ情報)を新規作成・初期化
    with open(encodeInfoFilePath, mode='w', encoding='UTF-16') as f:

        # 出力ファイルのヘッダ行を出力
        f.write(',,Before,,,,,,,,,,After,,,,,,,,' + '\r\n')
        f.write('FilePath,Diff,Encode,Artist,Album_Artist,Original_Artist,Album,disc_num,track_num,title,version,images,Encode,Artist,Album_Artist,Original_Artist,Album,disc_num,track_num,title' + '\r\n')

        # 変数の初期化 ()ディスクNo. トラックNo.更新用)
        preArtist = ''
        preAlbum = ''
        trackNo = 0

        # ターゲットファイルを一つずつ処理してゆく
        for i, targetFile in enumerate(targetFiles):

            # ターゲットファイルのパスをフルパス化
            targetFile = os.path.abspath(targetFile)
            print (str(i+1) + '/' + str(len(targetFiles)) + ' ' + targetFile)
            f.write('"' + targetFile + '"')

            # MP3タグ情報を取得する
            audioInfo = eyed3.load(targetFile)
            tag = audioInfo.tag
            if not tag:
                print('Info | NoTag')
                f.write(',"' + 'NoTag' + '"' + '\r\n')
                continue

            artist = tag.artist
            album_artist = tag.album_artist
            original_artist = tag.original_artist
            album = tag.album
            disc_num = tag.disc_num
            track_num = tag.track_num
            title = tag.title
            version = tag.version
            images = tag.images

            artist_2 = None
            album_2 = None
            title_2 = None
            album_artist_2 = None
            original_artist_2 = None

            # 1つ前のファイルと同じアーティスト名・アルバム名ならトラックナンバーを1つカウントアップ
            if( (artist != preArtist) or (album != preAlbum) ):
                trackNo = 1
            else:
                trackNo = trackNo + 1
            disc_num_2 = (None, None)
            track_num_2 = (trackNo, None)
            preArtist = artist
            preAlbum = album

            # タグ情報の文字コード変換
            enc1, enc2 = '', ''
            # 元々入力されていた文字列が UTF-16 の場合 (違う場合はExceptionが発生する)
            try:
                enc1, enc2 = 'utf-16', 'utf-16'
                if(artist is not None):
                    artist_2 = artist.encode(enc1).decode(enc2)
                if(album is not None):
                    album_2 = album.encode(enc1).decode(enc2)
                if(title is not None):
                    title_2 = title.encode(enc1).decode(enc2)
                if(album_artist is not None):
                    album_artist_2 = album_artist.encode(enc1).decode(enc2)
                if(original_artist is not None):
                    original_artist_2 = original_artist.encode(enc1).decode(enc2)
                #print('Converted from ' + enc1 + ' to ' +enc2)
            # 元々入力されていた文字が SJIS の場合 (違う場合はExceptionが発生する)
            except:
                try:
                    enc1, enc2 = 'latin1', 'cp932'
                    if(artist is not None):
                        artist_2 = artist.encode(enc1).decode(enc2)
                    if(album is not None):
                        album_2 = album.encode(enc1).decode(enc2)
                    if(title is not None):
                        title_2 = title.encode(enc1).decode(enc2)
                    if(album_artist is not None):
                        album_artist_2 = album_artist.encode(enc1).decode(enc2)
                    if(original_artist is not None):
                        original_artist_2 = original_artist.encode(enc1).decode(enc2)
                    enc1, enc2 = 'cp932', 'utf-16'
                    #print('Converted from ' + enc1 + ' to ' +enc2)
                # 元々入力されていた文字列が空欄の場合
                except:
                    enc1, enc2 = 'etc', 'etc'
                    artist_2 = artist
                    album_2 = album
                    title_2 = title
                    album_artist_2 = album_artist
                    original_artist_2 = original_artist
                    #print('Not Converted')

            # 文字コードの変更・ディスク番号・トラック番号の打ち直しによって、文字列に変化があったら Diff フラグを True にする
            diff, diffWord, diffNum = True, True, True
            if((artist == artist_2) and (album == album_2) and (title == title_2) and (album_artist == album_artist_2) and (original_artist == original_artist_2)):
                diffWord = False
            if((str(disc_num) == str(disc_num_2)) and (str(track_num) == str(track_num_2))):
                diffNum = False
            if((diffWord == False) and (diffNum == False)):
                diff = False
            #print(diff, diffWord, diffNum)

            # 出力ファイル(タグ情報)の出力
            f.write(',"' + str(diff) + '"')
            f.write(',"' + str(enc1) + '"')
            f.write(',"' + str(artist) + '"')
            f.write(',"' + str(album_artist) + '"')
            f.write(',"' + str(original_artist) + '"')
            f.write(',"' + str(album) + '"')
            f.write(',"' + str(disc_num) + '"')
            f.write(',"' + str(track_num) + '"')
            f.write(',"' + str(title) + '"')
            f.write(',"' + str(version) + '"')
            f.write(',"' + str(images) + '"')
            f.write(',"' + str(enc2) + '"')
            f.write(',"' + str(artist_2) + '"')
            f.write(',"' + str(album_artist_2) + '"')
            f.write(',"' + str(original_artist_2) + '"')
            f.write(',"' + str(album_2) + '"')
            f.write(',"' + str(disc_num_2) + '"')
            f.write(',"' + str(track_num_2) + '"')
            f.write(',"' + str(title_2) + '"')
            f.write('\r\n')

            # タグ情報の更新 (ユーザーが入力したタグ更新フラグが True の場合)
            if (updateTag == True):
                #audioInfo.tag.clear()
                # 文字を入力する領域に、文字コード変換前後で1つでも差異があった場合
                if (diffWord == True):
                    tag.artist = artist_2
                    tag.album_artist = album_artist_2
                    tag.original_artist = original_artist_2
                    tag.album = album_2
                    tag.title = title_2
                # 通し番号領域に差異があった場合
                if (diffNum == True):
                    tag.disc_num = disc_num_2
                    tag.track_num = track_num_2
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

# タグ情報の読み取りと更新
# updateTag=True:  タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新する
# updateTag=False: タグ情報一覧ファイルを出力後、MP3ファイルのタグ更新しない
ConvertTagInfo_SJIStoUTF16(logFilePath, convertMP3tag)

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
