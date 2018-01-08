#!/usr/bin/env bash
if [ $# != 1 ] ; then
   echo "using : bash start.sh workDir"
   exit 1
fi
wd=$1
cd wd
for file in `ls $wd`
do
        if [ -d $wd/$file ]
        then
                echo $file is dir
                continue
        else
                grep '^?' $file >test
                sort test|uniq>$file
                python amieResult.py $wd/$file
        fi
done