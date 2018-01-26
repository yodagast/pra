import pandas as pd
file="/home/shell/Documents/ "
d=open(file,'r')
out=open(file+".out",'w')
tmp=0
#awk -F'\t' '{print $6}' ./fbtriple.txt|sort|uniq -c|sort -k 1 -nr |head -45|awk '{print $NF}'>relations_to_run.tsv

for line in d.readlines():
    l=line.split("=>")
    if(len(l)<2):
        print(l)
        continue
    else:
        tmp=tmp+1
    str1=l[0].split("  ")
    str2=l[1].split("  ")
    if(str1[0].strip()==str2[2].strip() and str1[2].strip()==str2[0].strip()):
        if(len(str1[1])<40):
            out.write(str1[1]+"\n")
print(tmp)