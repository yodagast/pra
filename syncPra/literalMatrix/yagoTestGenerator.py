baseDir="/home/kdeapp/yago"

train=open(baseDir+"/triple.txt","r")

nd={}
ed={}
edge=baseDir+"/relation2id.txt"
node=baseDir+"/entity2id.txt"
entity=[]
with open(edge, 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        ed[s[0]]=int(s[1])
        entity.append(s[0])
        entity.append(s[1])
with open(node, 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        nd[s[0]]=int(s[1])

facts=open(baseDir+"/finalTrain.txt","r")
test=open(baseDir+"/finalTest.txt","w+")
with open(facts, 'r') as f:
    for line in f:
        s=line.replace("\n","").split('\t')
        if(s[0] in entity and s[1] in entity):
            #test.write(line)
            res=str(nd.get(s[0],0))+"\t"+str(nd.get(s[1],0)+"\t"+str(ed.get(s[1],0)))
res.close()