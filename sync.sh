#!/bin/bash
#code="/home/oem/pra"
#scp -r $code kdeapp@172.16.216.212:~/KBCompletion/code/
rsync -avz ./ kdeapp@172.16.216.188:/home/kdeapp/KBCompletion/code/pra/
