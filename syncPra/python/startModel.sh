#!/bin/bash
rm -f /home/kdeapp/KBCompletion/code/pra/examples/results/nell/final_emnlp2015/sfe_bfs_pra/*/scores.tsv
if [ $# -ge 1 ]; then
   model=$1
   nohup python praRegreesion.py $model> $model".out" 2>&1 &
   else
   nohup python praRegreesion.py > default.out 2>&1 &
fi

