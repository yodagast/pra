data="/home/kdeapp/KBCompletion/yago"
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
d=pd.read_csv(data+"/trainAll.txt",sep="\t",header=-1,names=["h","t","r"])
train,valid=train_test_split(d)
train.to_csv(data+"/train.txt",sep="\t",header=False,index=False)
valid.to_csv(data+"/valid.txt",sep="\t",header=False,index=False)
