#!/usr/bin/env bash

pwd="../fb15k/"
cd $pwd;
rm -rf $pwd/relation
rm -rf $pwd/splits
rm -rf $pwd/graphs
sed -i 's/[\r\s \t]*$//g' fbtrain.txt
sed -i 's/[ \t\r\s]*$//g' fbvalid.txt
sed -i 's/[ \t\r\s]*$//g' fbtest.txt
sed -i 's/[ \t\r\s]*$//g' relation2id.txt
sed -i 's/[ \t\r\s]*$//g' entity2id.txt
sed -i 's/[ \t\r\s]*$//g' fbtriple.txt
sed -i 's/[ \t\r\s]*$//g' fbattr.txt

sed -i 's/\.//g' fbtrain.txt
sed -i 's/\.//g' fbvalid.txt
sed -i 's/\.//g' fbtest.txt
sed -i 's/\.//g' relation2id.txt
sed -i 's/\.//g' entity2id.txt
sed -i 's/\.//g' fbtriple.txt
sed -i 's/\.//g' fbattr.txt

sed -i 's/\//_/g' fbtrain.txt
sed -i 's/\//_/g' fbvalid.txt
sed -i 's/\//_/g' fbtest.txt
sed -i 's/\//_/g' relation2id.txt
sed -i 's/\//_/g' entity2id.txt
sed -i 's/\//_/g' fbtriple.txt
sed -i 's/\//_/g' fbattr.txt

if [ ! -d "$pwd/relation" ]; then
  mkdir relation
fi
if [ ! -d "$pwd/splits" ]; then
  mkdir splits
  mkdir splits/fbSplit
fi
if [ ! -d "$pwd/graphs" ]; then
  mkdir graphs
  mkdir graphs/nell
  mkdir graphs/nell/kb_svo
  mkdir graphs/nell/kb_svo/graph_chi
fi
awk -F'\t' '{print $2"\t"$1}' ./relation2id.txt >./graphs/nell/kb_svo/edge_dict.tsv
awk -F'\t' '{print $2"\t"$1}' ./entity2id.txt >./graphs/nell/kb_svo/node_dict.tsv
printf "1\\n2\\n3\\n4\\n5"> ./graphs/nell/kb_svo/num_shards.tsv
awk -F'\t' '{print $1"\t"$2"\t"$3}' ./fbtriple.txt >./graphs/nell/kb_svo/graph_chi/edges.tsv
awk -F'\t' '{print $6}' ./fbtriple.txt|sort|uniq -c|sort -k 1 -nr |head -45|awk '{print $NF}'>./splits/fbSplit/relations_to_run.tsv
sed -i 's/[ \t\r\s]*$//g' ./splits/fbSplit/relations_to_run.tsv

while read line
do
      mkdir ./relation/$line
      mkdir ./splits/fbSplit/$line
done < ./splits/fbSplit/relations_to_run.tsv

while read line
do
    sed -n '/'$line'/p' fbtrain.txt>>train.txt
    sed -n '/'$line'/p' fbvalid.txt>>valid.txt
    sed -n '/'$line'/p' fbtest.txt>>test.txt
done < ./splits/fbSplit/relations_to_run.tsv


while read line
do
    sed -n '/'$line'/p' train.txt>>./graphs/nell/kb_svo/graph_chi/edges1.tsv
    sed -n '/'$line'/p' valid.txt>>./graphs/nell/kb_svo/graph_chi/edges1.tsv
    sed -n '/'$line'/p' test.txt>>./graphs/nell/kb_svo/graph_chi/edges1.tsv
done < ./splits/fbSplit/relations_to_run.tsv
awk -F'\t' '{print $1"\t"$2"\t"$3}' ./graphs/nell/kb_svo/graph_chi/edges1.tsv >./graphs/nell/kb_svo/graph_chi/edges.tsv

awk -F'\t' '{if(NR==1){name=$6}if(name!=$6){name=$6}; print $4"\t"$5>>"./relation/"name"/tra.tsv"}' train.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!=$6){name=$6} print $4"\t"$5 >>"./relation/"name"/val.tsv"}' valid.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!=$6){name=$6} print $4"\t"$5 >>"./relation/"name"/test.tsv"}' test.txt

awk -F'\t' '{if(NR==1){name=$6}if(name!= $6){name=$6} print $4"\t"$5>>"./relation/"name"/all.tsv"}' train.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!= $6){name=$6} print $4"\t"$5>>"./relation/"name"/all.tsv"}' valid.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!= $6){name=$6} print $4"\t"$5>>"./relation/"name"/all.tsv"}' test.txt

nohup python ../prepareData/generateNeg.py ../fb15k/> ../prepareData/myout.fb15k 2>&1 &
#ls ./yago/splits/*/test.tsv >./yago/splits/fbSplit/relations_to_run.tsv
#sed -i 's/\/test.tsv//g' yago/splits/yagoSplit/relations_to_run.tsv
#cp -r yago/graphs/ examples/
#cp -r yago/splits/ examples/
