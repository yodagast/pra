import sys,os
path="./saved_metrics.anyrel"
#if (len(sys.argv)<1):
#    path="./saved_metrics.anyrel"
#else:
path=sys.argv[1]
from collections import OrderedDict
d={}
resultFile=open(path,"r")
resCSV=open(path+".res","a+")
tmp=""
d1={}
for line in resultFile.readlines():
    line=line.replace("\n","").split("\t")
    if(tmp==""):
        tmp=line[1]
    if(tmp!=line[1]):
        d[tmp]=d1.copy()
        #print(d1.keys())
        #print(d1.values())
        d1={}
        tmp=line[1]
    d1[line[2]] = line[3]

resCSV.write("relation,MRR,MAP\n")
d=OrderedDict(sorted(d.items()))
for relation in d.keys():
    dd=d[relation]
    if(len(dd.keys())<3):
        continue
    if(relation=="__DATASET__"):
        resCSV.write(relation + "," + dd["MRR"] + "," + dd["MAP"] + "\n")
    else:
        print(dd["RR"] + "," + dd["AP"])
        resCSV.write(relation+","+dd["RR"] + "," + dd["AP"]+"\n")
resCSV.close()