#!/usr/bin/env bash
cd ..
ls ./fb15k/splits/fbSplit/*/testing.tsv >./fb15k/splits/fbSplit/relations_to_run.tsv
sed -i 's/\/testing\.tsv//g' fb15k/splits/fbSplit/relations_to_run.tsv
sed -i 's/\.\/fb15k\/splits\/fbSplit\///g' fb15k/splits/fbSplit/relations_to_run.tsv
rm -r examples/graphs_bak/*
rm -r examples/splits_bak/*
mv  examples/graphs/ examples/graphs_bak
mv examples/splits/ examples/splits_bak
cp -r fb15k/graphs/ examples/
cp -r fb15k/splits/ examples/