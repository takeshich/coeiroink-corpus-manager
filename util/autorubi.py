#!/usr/local/bin/python3
# -*- coding: utf_8 -*-
#以下のブログより使用。ライセンス等は不明
#https://www.karelie.net/python3-mecab-html-furigana-5/

import sys
import MeCab
import re
import jaconv
import os



def henkan(text):
    kana = jaconv.kata2hira(text)
    return kana
def tohensu(origin, kana):
    origin = "".join(origin)
    kana = "".join(kana)
    return origin, kana
def kanadelete(origin, kana):
    origin = list(origin)
    kana = list(kana)
    num1 = len(origin)
    num2 = len(kana)
    okurigana = ""
    if origin[num1-1] == kana[num2-1] and origin[num1-2] == kana[num2-2]:
        okurigana = origin[num1-2]+origin[num1-1]
        origin[num1-1] = ""
        origin[num1-2] = ""
        kana[num2-1] = ""
        kana[num2-2] = ""
        origin, kana = tohensu(origin, kana)
    elif origin[num1-1] == kana[num2-1]:
        okurigana = origin[num1-1]
        origin[num1-1] = ""
        kana[num2-1] = ""
        origin = "".join(origin)
        kana = "".join(kana)
    else:
        origin, kana = tohensu(origin, kana)
    return origin, kana, okurigana
def kanji_kana(origin, kana):
    # 仮名を基準に分割
    origin_split = re.split(r'([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
    # 不要な空白を削除
    origin_split = [x.strip() for x in origin_split if x.strip()]
    # 片仮名を仮名にする
    origin_split_1_kana = henkan(origin_split[1])
    # 「送り仮名」を含んだ「読み仮名」から「送り仮名」を後方一致で削除する
    kana = kana.rstrip(origin_split_1_kana)
    # それぞれ分割したものをHTMLのタグに挿入する
    print(
        "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(origin_split[0], kana), end="")
    print(origin_split[1], end="")
def kana_kanji(origin, kana):
    # 仮名を基準に分割
    origin_split = re.split(r'([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
    # 不要な空白を削除
    origin_split = [x.strip() for x in origin_split if x.strip()]
    # 片仮名を仮名にする
    origin_split_0_kana = henkan(origin_split[0])
    # 「行頭の仮名」を含んだ「読み仮名」から「行頭の仮名」を前方一致で削除する
    kana = kana.lstrip(origin_split_0_kana)
    # それぞれ分割したものをHTMLのタグに挿入する
    print(origin_split[0], end="")
    print(
        "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(origin_split[1], kana), end="")
def kanji_kana_kanji(origin, kana):
    # 漢字を基準に分割
    origin_split = re.split(r'([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
    # 不要な空白を削除
    origin_split = [x.strip() for x in origin_split if x.strip()]
    # 両端から１文字削除（精度を高めるため）
    kana_delete = kana[1:]
    kana_delete = kana_delete[:-1]
    # 両端から１文字削除したものの中に該当する仮名がいくつ存在するか確認し（２文字以上存在する場合、この処理の正確性が欠けるため）条件を満たす場合のみ分割しルビを振る
    if kana_delete.count(origin_split[1]) == 1:
        # 片仮名を仮名にする
        origin_split_1_kana = henkan(origin_split[1])
        # 該当する仮名で分割
        kana_split = re.split(u'(' + origin_split_1_kana + ')', kana)
        print(
            "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>{2}<ruby><rb>{3}</rb><rt>{4}</rt></ruby>".format(origin_split[0], kana_split[0], origin_split[1], origin_split[2], kana_split[2]), end="")
    # 条件を満たさない場合は分割せずにルビを振る
    else:
        print(
            "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(origin, kana), end="")
def kanji_kana_kanji_kana(origin, kana):
    # 仮名を基準に分割
    origin_split = re.split(r'([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
    # 不要な空白を削除
    origin_split = [x.strip() for x in origin_split if x.strip()]
    # 行頭から１文字削除（精度を高めるため）
    kana_delete = kana[1:]
    # 行頭から１文字削除したものの中に該当する仮名がいくつ存在するか確認し（２文字以上存在する場合、この処理の正確性が欠けるため）条件を満たす場合のみ分割しルビを振る
    if kana_delete.count(origin_split[1]) == 1 and kana_delete.count(origin_split[3]) == 1:
        # 片仮名を仮名にする
        origin_split_1_kana = henkan(origin_split[1])
        origin_split_3_kana = henkan(origin_split[3])
        kana_split = re.split(
            u'(' + origin_split_1_kana + '|' + origin_split_3_kana + ')', kana)
        kana_split = [x.strip() for x in kana_split if x.strip()]
        # print(kana_split)
        # print(origin_split)
        print(
            "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>{2}<ruby><rb>{3}</rb><rt>{4}</rt></ruby>{5}".format(origin_split[0], kana_split[0], origin_split[1], origin_split[2], kana_split[2], origin_split[3]), end="")
    # 条件を満たさない場合は分割せずにルビを振る
    else:
        print(
            "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(origin, kana), end="")
def kana_kanji_kana(origin, kana):
    # 仮名を基準に分割
    origin_split = re.split(r'([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
    # 不要な空白を削除
    origin_split = [x.strip() for x in origin_split if x.strip()]
    # 片仮名を仮名にする
    origin_split_0_kana = henkan(origin_split[0])
    origin_split_2_kana = henkan(origin_split[2])
    # 読み仮名の行頭から始めの仮名を削除
    kana = kana.lstrip(origin_split_0_kana)
    # 読み仮名の行末から最後の仮名を削除
    kana = kana.rstrip(origin_split_2_kana)
    print(
        "{0}<ruby><rb>{1}</rb><rt>{2}</rt></ruby>{3}".format(origin_split[0], origin_split[1], kana, origin_split[2]), end="")

#引数チェック
if len(sys.argv) < 2:
    sys.exit("対象のファイル名を入力してください。")
if len(sys.argv) > 3:
    sys.exit("対象のファイルは一つのみ有効です。")
file_path = sys.argv[1]

#絶対パス
path = os.path.abspath(file_path)

#存在チェック
if not os.path.isfile(path):
    sys.exit("対象ファイルが存在しません。")

with open(path, "r", encoding="utf-8") as f:
    for i in f:
        mecab = MeCab.Tagger("-Ochasen")
        #mecab = MeCab.Tagger(
        #    "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")
        mecab.parse('')  # 空でパースする必要がある
        node = mecab.parseToNode(i)
        # node = mecab.parseToNode("魔法少女リリカルなのは")
        # node = mecab.parseToNode("160立方メートル")
        while node:
            origin = node.surface  # もとの単語を代入
            # アルファベットや数字など読み仮名が存在しない場合にエラーになるので読み仮名が存在する時のみ代入させる
            if node.feature.split(",")[7:]:
                # 読み仮名を代入
                yomi = node.feature.split(",")[7]
                kana = henkan(yomi)
            # 正規表現で漢字と一致するかをチェック
            pattern = "[一-龥]"
            matchOB = re.search(pattern, origin)
            # originが空のとき、漢字以外の時はふりがなを振る必要がないのでそのまま出力する
            if origin != "" and matchOB:
                # 正規表現で「漢字+仮名」かどうかチェック
                matchOB_kanji_kana = re.fullmatch(
                    r'(^[一-龥]+)([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
                # 正規表現で「仮名+漢字」かどうかチェック
                matchOB_kana_kanji = re.fullmatch(
                    r'(^[\u3041 -\u3093\u30A1-\u30FC]+)([一-龥]+|)', origin)
                # 正規表現で「仮名+漢字」かどうかチェック
                matchOB_kanji_kana_kanji = re.fullmatch(
                    r'(^[一-龥]+)([\u3041 -\u3093\u30A1-\u30FC]+)([一-龥]+)', origin)
                # 正規表現で「漢字+仮名+漢字+仮名」かどうかチェック
                matchOB_kanji_kana_kanji_kana = re.fullmatch(
                    r'(^[一-龥]+)([\u3041 -\u3093\u30A1-\u30FC]+)([一-龥]+)([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
                # 正規表現で「仮名+漢字+仮名」かどうかチェック
                matchOB_kana_kanji_kana = re.fullmatch(
                    r'(^[\u3041 -\u3093\u30A1-\u30FC]+)([一-龥]+)([\u3041 -\u3093\u30A1-\u30FC]+)', origin)
                if origin != "" and matchOB_kanji_kana:
                    kanji_kana(origin, kana)
                # 正規表現で「仮名+漢字」の場合
                elif origin != "" and matchOB_kana_kanji:
                    kana_kanji(origin, kana)
                elif origin != "" and matchOB_kanji_kana_kanji:
                    kanji_kana_kanji(origin, kana)
                elif origin != "" and matchOB_kanji_kana_kanji_kana:
                    kanji_kana_kanji_kana(origin, kana)
                elif origin != "" and matchOB_kana_kanji_kana:
                    kana_kanji_kana(origin, kana)
                else:
                    origin, kana, okurigana = kanadelete(origin, kana)
                    print(
                        "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(origin, kana), end="")
                    print(okurigana, end="")
            else:
                print(origin, end="")
            node = node.next
        print('\n')
