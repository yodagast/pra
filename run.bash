#!/bin/bash
#rm -rf /home/kdeapp/KBCompletion/code/pra/examples/splits/yagoSplit/*
#cp -r ~/KBCompletion/Data/matrix1/* /home/kde/KBCompletion/code/pra/examples/splits/yagoSplit/
#cp /home/kde/KBCompletion/code/pra/examples/splits/params.json /home/kde/KBCompletion/code/pra/examples/splits/yagoSplit/params.json
#cp /home/kde/KBCompletion/code/pra/examples/splits/relations_to_run.tsv /home/kde/KBCompletion/code/pra/examples/splits/yagoSplit/
## using in 212
rm -rf ./examples/results/*
sbt 'run /home/yhuang/java/pra/examples/ sfe_bfs_pra.json'
