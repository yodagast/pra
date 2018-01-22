#!/usr/bin/env bash
cd ..
ls ./yago/splits/yagoSplit/*/testing.tsv >./yago/splits/yagoSplit/relations_to_run.tsv
sed -i 's/\/testing\.tsv//g' yago/splits/yagoSplit/relations_to_run.tsv
sed -i 's/\.\/yago\/splits\/yagoSplit\///g' yago/splits/yagoSplit/relations_to_run.tsv
rm -r examples/graphs_bak/*
rm -r examples/splits_bak/*
mv  examples/graphs/ examples/graphs_bak
mv examples/splits/ examples/splits_bak
cp -r yago/graphs/ examples/
cp -r yago/splits/ examples/