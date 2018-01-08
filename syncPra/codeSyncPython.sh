#!/bin/bash
#code="/home/oem/pra"
#scp -r $code kdeapp@172.16.216.212:~/KBCompletion/code/
#rsync -avz /home/oem/pra/src/ kdeapp@172.16.216.212:/home/kdeapp/KBCompletion/code/pra/src/

rsync -avz /home/oem/PycharmProjects/syncPra/python/ kdeapp@172.16.216.212:/home/kdeapp/KBCompletion/python/

# 替换以\t开头的前两列
# sed -i 's/[^ ]*\t//' test

#获取所有的正例 使用MAP进行计算
#awk -F'\t' '$3>0 {print $1"\t"$2"\t"FILENAME}' */train.tsv >>train.txt
#sed -i 's/\/train\.tsv//g' train.txt
#awk -F'\t' '$3>0 {print $1"\t"$2"\t"FILENAME}' */testing.tsv >>test.txt
#sed -i 's/\/test\.tsv//g' test.txt
#sed -i 's/[<>]//g' train.txt

