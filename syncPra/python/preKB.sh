#!/bin/bash
###读取当前目录下的yagoFacts文件 按列进行切分成获得edge_dict.tsv和node_dict.tsv保存在graph文件夹下
### 运行当前路径下的mkGraph.py文件 获得graph/graph_chi文件夹
if [ $# != 1 ] ; then 
   echo "using : bash preKB.sh yagoFacts.tsv"
   exit 1
fi
file=$1
pwd=`pwd`
cd $pwd;
if [ ! -d "$pwd/relation" ]; then
  mkdir relation
fi
if [ ! -d "$pwd/graph" ]; then
  mkdir graph
fi
 
read col <<< `head $file| awk -F'\t' 'END{print NF}'`
if [ $col -ge 4 ]; then
   cut -f2-4 $file>$file".new"
   mv $file".new"  $file
   sed -i "s/[<>]//g" $file
fi
read col<<< `head $file| awk -F'\t' 'END{print NF}'`
if [ $col -ne 3 ]; then
    echo "$col are too many columns!"
    exit 1
fi
awk -F'\t' '{print $2}' $file |sort|uniq >./graph/r.tsv
awk -F'\t' '{print NR"\t"$1}' ./graph/r.tsv >./graph/edge_dict.tsv
rm ./graph/r.tsv
awk -F'\t' '{print $1"\n"$3}' $file |sort|uniq >./graph/node.tsv
awk -F'\t' '{print NR"\t"$1}' ./graph/node.tsv >./graph/node_dict.tsv
rm ./graph/node.tsv
wc -l ./graph/edge_dict.tsv
wc -l ./graph/node_dict.tsv
rm -f ./relation/*
awk -F'\t' '{if(NR==1){name=$2}if(name != $2){name=$2} print $1"\t"$3 >>"relation/"name".tsv"}' $file
rename 's/[<>]//g' ./relation/*
rm -f $pwd"/graph/graph/graph_chi/edges.tsv"
python triple2id.py $pwd

if [ ! -d "$pwd/splits" ]; then
  mkdir splits
fi
rm -rf $pwd"/splits/*"
python geneNegTriple.py $pwd