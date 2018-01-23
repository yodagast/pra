#!/usr/bin/env bash
pwd="../yago/"
cd $pwd;
awk -F'\t' '{print $5}' ./yagoattr.txt|sort|uniq -c >./literalDict.txt