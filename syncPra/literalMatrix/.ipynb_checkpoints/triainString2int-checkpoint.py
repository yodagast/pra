import os
pwd="/home/kdeapp/yago"
node=pwd+"/entity2id.txt"
edge=pwd+"/relation2id.txt"
ed={}
nd={}
ed={}
nd={}
import os
with open(edge, 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        ed[s[0]]=int(s[1])
with open(node, 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        nd[s[0]]=int(s[1])

d=open(pwd+"/finalTrain.txt","r")
fout=open(pwd+"/triple2int.txt","w+")
for line in d.readlines():
    s = line.replace("\n", "").split('\t')
    fout.write(str(nd.get(s[0],0)))
    fout.write("\t")
    fout.write(str(nd.get(s[2], 0)))
    fout.write("\t")
    fout.write(str(ed.get(s[1], 0)))
    #res = str(nd.get(s[0],0)) + "\t" + str(nd.get(s[1], 0)) + "\t" + str(ed.get(s[2], 0)))
    fout.write("\n")
fout.close()