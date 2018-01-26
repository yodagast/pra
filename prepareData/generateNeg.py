import pandas as pd
import sys,os
import numpy as np
np.random.seed(1)
base=sys.argv[1]
print(base)
if("fb" in base):
    dir=base+"/splits/fbSplit/"
else:
    dir=base+"/splits/yagoSplit/"
rel_dir=base+"/relation/"
def geneNegPair(train_df,all_df,relation,negRate=4,onlyTailer=False,isTrain=False):
    if(train_df.shape[0]<20 or all_df.shape[0]<20):
        return;
    splits_relation_path=os.path.join(os.path.abspath(dir),relation)
    print(splits_relation_path)
    train_df["class"]=1
    res=pd.DataFrame()
    for index,data in train_df.iterrows():
        h=data['source']
        t=data['target']
        falseRow=all_df.sample(n=min(negRate,train_df.shape[0]),replace=False).reset_index(drop=True)
        list=[]
        for ind1,d1 in falseRow.iterrows():
            if(d1['source']==h and d1['target']==t):
                list.append(ind1)
        falseRow.drop(list,inplace=True)
        if(onlyTailer):
            falseRow.loc[0:negRate,['target']]=t
        else:
            falseRow.loc[0:negRate/2-1,['source']]=h
            falseRow.loc[negRate/2:negRate,['target']]=t
        falseRow["class"]=-1
        res=res.append([data.to_frame().T,falseRow],ignore_index=True)
    list=rmPostivePairs(all_df=all_df,res_df=res)
    res.drop(list,inplace=True)
    if(isTrain):
        res.to_csv(splits_relation_path+"/training.tsv",sep="\t",index=False,header=False)
    else:
        res.to_csv(splits_relation_path+"/testing.tsv",sep="\t",index=False,header=False)


def rmPostivePairs(all_df,res_df):
    list1=[]
    pos_list=[]
    for index,data in all_df.iterrows():
        ss=data['source']+data['target']
        pos_list.append(ss)
    for ind1,d1 in res_df.iterrows():
        if(d1['class']>0):
            continue
        else:
            ss=d1['source']+d1['target']
            if ss in pos_list:
                list1.append(ind1)
    return list1

import multiprocessing as mp
pool = mp.Pool(processes = (mp.cpu_count() - 1))

for relation in os.listdir(os.path.abspath(rel_dir)):
    abs_relation_path=os.path.join(os.path.abspath(rel_dir),relation)
    print(abs_relation_path)
    if(os.path.exists(abs_relation_path+"/tra.tsv")):
        train=pd.read_csv(abs_relation_path+"/tra.tsv",header=-1,sep='\t',names=['source','target'])
    if(os.path.exists(abs_relation_path+"/test.tsv")):
        test=pd.read_csv(abs_relation_path+"/test.tsv",header=-1,sep='\t',names=['source','target'])
    if(os.path.exists(abs_relation_path+"/all.tsv")):
        all=pd.read_csv(abs_relation_path+"/all.tsv",header=-1,sep='\t',names=['source','target'])
    p1=mp.Process(target=geneNegPair, args = (train,all,relation),kwargs={"isTrain":True})
    p2=mp.Process(target=geneNegPair, args = (test,all,relation),kwargs={"isTrain":False})
    #pool.apply_async(geneNegPair, args = (train,all,relation,),kwargs={"isTrain":True})
    #pool.apply_async(geneNegPair, args = (train,all,relation,),kwargs={"isTrain":False})
    #geneNegPair(train,all,relation,isTrain=True)
    #geneNegPair(test,all,relation)
    p1.start()
    p2.start()
    p1.join()
    p2.join()






