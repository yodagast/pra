#!/usr/bin/env bash

cut -f2-4 yagoLiteralFacts.tsv >yagoLiteral.tsv
awk -F"\^\^" '{print $1}' yagoLiteral.tsv >literal.tsv
sed -i 's/[""]//g' literal.tsv
sed -i '/rdfs:/d' literal.tsv
awk -F"\t" '{print $2}' literal.tsv|sort|uniq>literalDict.txt
