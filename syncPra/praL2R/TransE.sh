#!/usr/bin/env bash
path="/home/kdeapp/KBCompletion/code/pra/examples/splits/yagoSplit"
cd $path
awk -F'\t' '$3>0 {print $1"\t"$2"\t"FILENAME}' */training.tsv >>train.txt
sed -i 's/\/training\.tsv//g' train.txt
awk -F'\t' '$3>0 {print $1"\t"$2"\t"FILENAME}' */testing.tsv >>test.txt
sed -i 's/\/testing\.tsv//g' test.txt
sed -i 's/[<>]//g' train.txt
sed -i 's/[<>]//g' test.txt
path1="/home/kdeapp/KBCompletion/python/"
cd $path1
mkdir data
cp $path"/train.txt" $path1
cp $path"/test.txt" $path1
awk -F"\t" '{print $2"\t"$1-1}' entity2id.txt> e.txt
mv e.txt entity2id.txt
awk -F"\t" '{print $2"\t"$1-1}' relation2id.txt>r.txt
mv r.txt relation2id.txt
