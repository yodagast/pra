import pandas as pd
import sklearn,sys,os
import numpy as np
from sklearn import metrics
path="/home/kdeapp/KBCompletion/code/pra/examples/results_yago/nell/final_emnlp2015/sfe_bfs_pra/"
def getLabel(x):
    if(x=='*'):
        return 1
    else:
        return 0
def sigmoid(x):
    return 1/(1+np.exp(-x))

for relation in os.listdir(path):
    score=os.path.join(path,relation+"/scores.tsv")
    df=pd.read_csv(score,header=-1,sep='\t',names=['s','t','y_pred','label'])
    df["y_true"]=df["y_true"].apply(getLabel).as_matrix()
    df["y_pred"]=df["y_pred"].apply(sigmoid).as_matrix()
    #df.dropna(inplace=True)
    fpr, tpr, thresholds = metrics.roc_curve(df["y_true"],df["y_pred"], pos_label=2)
    auc=metrics.auc(fpr,tpr)
    print("%s\tauc score %f",relation,auc)

