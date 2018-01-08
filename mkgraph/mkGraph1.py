#!/home/kdeapp/anaconda3/bin/python3.6
### 读取yagoFacts.tsv，对每个关系生成training &test文件，并随机生成负例
import sys
if (len(sys.argv) < 2):
    print("use : python $pwd")
    sys.exit()
pwd = sys.argv[1]
import random

graph = pwd + "/"
import os
import pandas as pd
from sklearn.model_selection import train_test_split

fact = pwd + "/yagoFacts.tsv"
fact = pd.read_csv(fact, header=-1, sep='\t', names=['source', 'relation', 'target'])
del fact['relation']
fact['class'] = -1


def mkRandomTriple(file):
    relation = pd.read_csv(graph + "relation/" + file, header=-1, sep='\t', names=['source', 'target'])
    relation["class"] = 1
    train, test = train_test_split(relation, test_size=0.2)
    string = graph + "splits/" + file.replace(".tsv", "")
    if (os.path.exists(graph + "splits/") == False):
        os.mkdir(graph + "splits/")
    if (os.path.exists(string) == False):
        print(string)
        os.mkdir(string)
    train = geneNeg1(train)
    test = geneNeg1(test)
    train.to_csv(string + "/train.tsv", sep="\t", index=False, header=False)
    test.to_csv(string + "/test.tsv", sep="\t", index=False, header=False)


def geneNeg1(df):
    negCnt = 2
    res = pd.DataFrame()
    for index, data in df.iterrows():
        h = data['source']
        t = data['target']
        falseRow = fact.sample(n=negCnt, replace=False)
        falseRow.loc[0:negCnt / 2, ['source']] = h
        falseRow.loc[negCnt / 2 + 1:negCnt, ['target']] = t
        res = res.append([data.to_frame().T, falseRow], ignore_index=True)
    return res.drop_duplicates()

for file in os.listdir(graph + "relation/"):
    # relation=os.path.join(graph+"relation/",file)
    mkRandomTriple(file)