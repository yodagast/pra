import os,sys
fileName=sys.argv[1]
DataDir="/home/oem/Documents/PRAResult/rulelearningresults/"
d={}
d1={}
if(fileName.find(".uniq")>0):
    exit(0)
f=open(fileName,"r")
for line in f.readlines():
    line=line.replace("\n","")
    num=0
    if(line.find("?b")>0):
        num=line.rfind("?b")
    if(line.find("=>")<1):
        continue
    key=line[:num+3].strip()
    val=line[num+3:].strip()
    print(key+"\t"+val)
    if(key in d.keys() or val in d1.keys()):
        continue
    d[key]=val
    d1[val]=key

f1=os.path.join(DataDir,fileName+".uniq")
file1=open(f1,"w")
print(len(d.keys()))
for key in d.keys():
    file1.write(key+"\t"+d[key]+"\n")




