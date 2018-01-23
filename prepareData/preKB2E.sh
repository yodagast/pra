#!/usr/bin/env bash

pwd="../yago/"
cd $pwd;
rm -rf $pwd/relation
rm -rf $pwd/splits
rm -rf $pwd/graphs
sed -i 's/[\r\s \t]*$//g' yagotrain.txt
sed -i 's/[ \t\r\s]*$//g' yagovalid.txt
sed -i 's/[ \t\r\s]*$//g' yagotest.txt
sed -i 's/[ \t\r\s]*$//g' relation2id.txt
sed -i 's/[ \t\r\s]*$//g' entity2id.txt
sed -i 's/[ \t\r\s]*$//g' yagotriple.txt
sed -i 's/[ \t\r\s]*$//g' yagoattr.txt
if [ ! -d "$pwd/relation" ]; then
  mkdir relation
fi
if [ ! -d "$pwd/splits" ]; then
  mkdir splits
  mkdir splits/yagoSplit
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
awk -F'\t' '{print $1"\t"$2"\t"$3}' ./yagotriple.txt >./graphs/nell/kb_svo/graph_chi/edges.tsv
awk -F'\t' '{print $6}' ./yagotriple.txt|sort|uniq >./splits/yagoSplit/relations_to_run.tsv
sed -i 's/[ \t\r\s]*$//g' ./splits/yagoSplit/relations_to_run.tsv
while read line
do
      mkdir ./relation/$line
      mkdir ./splits/yagoSplit/$line
done < ./splits/yagoSplit/relations_to_run.tsv

awk -F'\t' '{if(NR==1){name=$6}if(name!=$6){name=$6}; print $4"\t"$5>>"./relation/"name"/tra.tsv"}' yagotrain.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!=$6){name=$6} print $4"\t"$5 >>"./relation/"name"/val.tsv"}' yagovalid.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!=$6){name=$6} print $4"\t"$5 >>"./relation/"name"/test.tsv"}' yagotest.txt

awk -F'\t' '{if(NR==1){name=$6}if(name!= $6){name=$6} print $4"\t"$5>>"./relation/"name"/all.tsv"}' yagotrain.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!= $6){name=$6} print $4"\t"$5>>"./relation/"name"/all.tsv"}' yagovalid.txt
awk -F'\t' '{if(NR==1){name=$6}if(name!= $6){name=$6} print $4"\t"$5>>"./relation/"name"/all.tsv"}' yagotest.txt

nohup python ../prepareData/generateNeg.py ../yago/> ../prepareData/myout.file 2>&1 &
#ls ./yago/splits/*/test.tsv >./yago/splits/yagoSplit/relations_to_run.tsv
#sed -i 's/\/test.tsv//g' yago/splits/yagoSplit/relations_to_run.tsv
#cp -r yago/graphs/ examples/
#cp -r yago/splits/ examples/