import pandas as pd
baseDir="/home/kdeapp/yago"
train=baseDir+"/yagoFacts_3.tsv"
test=baseDir+"/test.txt"
train=open(train,"r")
test=open(test,"r")
#fout=open(baseDir+"/finalTest.txt","w+")
fout1=open(baseDir+"/finalTrain.txt","w+")
X=[]
e=[]
for line in test.readlines():
    #tmp = line.replace("\n", "").split("\t")
    X.append(line)
for line in train.readlines():
    if(line in X):
        continue
    else:
        fout1.write(line)
#fout.close()
fout1.close()