#!/bin/bash

# 入力ファイルのパスを格納する変数を定義する
#input_file="../mana-corpus/mana-corpus-aisatsu-kana.txt"
#input_file="../mana-corpus/mana-corpus-question-kana.txt"
#input_file="../mana-corpus/mana-corpus-question2-kana.txt"
input_file="../mana-corpus/mana-corpus-setsuzoku-kana.txt"

# 出力ファイルの接頭辞を格納する変数を定義する
#prefix="AISATSU_"
#prefix="QUESTION_"
#prefix="QUESTION2_"
prefix="SETSUZOKU_"

# 出力ファイルのパスを格納する変数を定義する
output_dir="../mana-corpus/formmvc"

# インデックスを初期化する
index=1

# テキストファイルを読み込む
for line in $(cat "$input_file"); do
	# 1行ずつ出力する
	printf -v output_file "%s/%s%03d.txt" $output_dir $prefix $index
	echo "$line" >> "$output_file"

	# インデックスをインクリメントする
	index=$((index+1))
done
