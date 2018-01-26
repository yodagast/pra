import pandas as pd
import sklearn,sys,os
import numpy as np
from sklearn import metrics
model=sys.argv[1]
#path="/home/kdeapp/KBCompletion/code/pra/fb15k/results/nell/final_emnlp2015/"+model+"/"
#out="/home/kdeapp/KBCompletion/code/pra/fb15k/results/nell/final_emnlp2015/"+model+".tsv"
path="/home/kdeapp/KBCompletion/code/pra/yago/results/nell/final_emnlp2015/"+model+"/"
out="/home/kdeapp/KBCompletion/code/pra/yago/results/nell/final_emnlp2015/"+model+".tsv"
outFile=open(out,"w")
def getLabel(x):
    if(x=='*'):
        return 1
    else:
        return 0
def sigmoid(x):
    return 1/(1+np.exp(-x))

def getMetrics(df):
    mr=0
    hit1=0
    cnt=0
    pos=0
    for idx,data in df.iterrows():
        if(cnt==0 and data["y_true"]>0 ):
            hit1=1
        cnt=cnt+1
        if(data["y_true"]>0):
            mr=cnt+mr
            pos=pos+1
    if(pos==0 or mr==0):
        return cnt,hit1
    return float(mr/pos),hit1


def mrr_hit1(df):
    cnt=0
    mrr=0
    hit1=0
    for key,group in df.groupby(["s"]):
        mr,hit=getMetrics(group.sort_values(by='y_pred', ascending=False))
        mrr=mrr+mr
        hit1=hit1+hit
        cnt=cnt+1
    return float(mrr/cnt),float(hit1/cnt)

for relation in os.listdir(path):
    if("log" in relation or "param" in relation or "relations_to_run" in relation):
        continue
    score=os.path.join(path,relation+"/scores.tsv")
    if(os.access(score,os.F_OK))==False:
        continue
    df=pd.read_csv(score,header=-1,sep='\t',names=['s','t','y_pred','y_true'])
    df["y_true"]=df["y_true"].apply(getLabel).as_matrix()
    df["y_pred"]=df["y_pred"].apply(sigmoid).as_matrix()
    #df.dropna(inplace=True)
    fpr, tpr, thresholds = metrics.roc_curve(df["y_true"],df["y_pred"])
    auc=metrics.auc(fpr,tpr)
    mrr,hit1=mrr_hit1(df)
    res1="{}\t AUC {}".format(relation,auc)
    print(res1,end="\t")
    res2="MR {}\t hit@1 {}".format(mrr,hit1)
    print(res2)
    outFile.write(res1+"\t"+res2+"\n")
