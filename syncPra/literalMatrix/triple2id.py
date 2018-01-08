#!/home/kdeapp/anaconda3/bin/python3.6
import sys
if(len(sys.argv)<2):
    print("use : python $pwd")
    sys.exit()
pwd=sys.argv[1]    
node=pwd+"/graph/node_dict.tsv"
edge=pwd+"/graph/edge_dict.tsv"
graph=pwd+"/"
ed={}
nd={}
import os
with open(edge, 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        ed[s[1]]=int(s[0])
with open(node, 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        nd[s[1]]=int(s[0])
if(os.path.exists(graph+"graph/graph_chi") ==False):
    os.mkdir(graph+"graph/graph_chi")
edges=open(graph+"graph/graph_chi/edges.tsv","w")
facts=open(graph+"yagoFacts.tsv")
with open(graph+"yagoFacts.tsv", 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        res=str(nd.get(s[0],"error"))+"\t"+str(nd.get(s[2],"error")+"\t"+str(ed.get(s[1],"error")))
        edges.write(res+"\n")
edges.close()
