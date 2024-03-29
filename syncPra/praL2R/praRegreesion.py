import os,sys
import xgboost as xgb
import mxnet as mx
import pandas as pd
import numpy as np
from fastFM import als
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import roc_auc_score
from sklearn.datasets import load_svmlight_files
from sklearn.linear_model import LogisticRegression, SGDRegressor,SGDClassifier

if(len(sys.argv)<2):
    model="xgb"
else:
    model=sys.argv[1]
#path = "/home/kdeapp/KBCompletion/code/pra/yago/matrix/"
#baseDir = "/home/kdeapp/KBCompletion/code/pra/yago/results/nell/final_emnlp2015/sfe_bfs_pra_anyrel_"+model+"/"
path = "/home/kdeapp/KBCompletion/code/pra/yago/matrix/"
baseDir = "/home/kdeapp/KBCompletion/code/pra/yago/results/nell/final_emnlp2015/sfe_bfs_pra_"+model+"/"
os.mkdir(baseDir)
print("using model:"+model,end="\t")

def writeScoresInPraStyle(test_pair, train_list, relation):
    '''
    :param test_pair: DataFrame {source,target,class,score}
    :param train_list: list(head,relation,tail)
    :param relation: relationNames
    :return: {source,target,score,mark}
    '''
    writer = open(baseDir + relation + "/scores.tsv", "a+")
    res = test_pair.sort_values(["source", "score"],ascending=[True,False])#.groupby(["source"]).apply(lambda x: x)
    res["mark"] = ""
    for index, data in res.iterrows():
        writer.write(data["source"] + "\t" + data["target"] + "\t" + str(data["score"]))
        string = data["source"].strip()+ ","+data["target"].strip()+","+str(data["class"]).strip()
        if (string in train_list):
            data["mark"] = "*"
        elif (data["class"] > 0):
            data["mark"] = "^"
        writer.write("\t" + data["mark"] + "\n")
    writer.close()

def praRegression(model,dirName,X_train,y_train,X_test,y_test,train_pair,test_pair):
    if(model=="lr"):
        reg=LogisticRegression(penalty="l1",n_jobs=-1)
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
    elif(model=="sgdregressor"):
        reg =SGDRegressor(penalty='elasticnet',n_iter=500,l1_ratio=0.6)
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
    elif(model=="fastFM"):
        reg = als.FMRegression(n_iter=1000, init_stdev=0.1, rank=2, l2_reg_w=0.1, l2_reg_V=0.5)
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
    elif(model=="gbr"):
        reg=GradientBoostingRegressor(n_estimators=100)
        reg.fit(X_train.toarray(), y_train)
        y_pred = reg.predict(X_test)
    elif(model=="xgb"):
        X_train=X_train.tocsc()
        X_test=X_test.tocsc()
        reg = xgb.XGBRegressor(max_depth=7,objective="rank:pairwise", learning_rate=0.08,
                               subsample=0.8,colsample_bytree=0.7, reg_alpha=0.6,reg_lambda=0.1,n_estimators=1500)
        reg.fit(X_train,y_train)
        y_pred = reg.predict(X_test)
    elif(model=="mxnet"):
        y_pred=mxTrainer(dirName,X_train,y_train,X_test,y_test,train_pair,test_pair)
    else:
        exit(1)
    #y_pred = reg.predict(X_test)
    test_pair['score'] = y_pred
    print(roc_auc_score(y_true=y_test, y_score=y_pred))
    writeScoresInPraStyle(test_pair, train_pair, dirName)


def rankNet():
    X = mx.sym.Variable('data')
    op = mx.symbol.Dropout(data=X, name='dp3', p=0.2)
    label = mx.sym.Variable(name='softmax_label')
    fc1 = mx.sym.FullyConnected(data=op, num_hidden=128)
    act1 = mx.symbol.Activation(data=fc1, name='relu1', act_type="relu")
    fc2 = mx.symbol.FullyConnected(data=act1, name='fc2', num_hidden=64)
    act2 = mx.symbol.Activation(data=fc2, name='relu2', act_type="relu")
    #fc3 = mx.symbol.FullyConnected(data=act2, name='fc3', num_hidden=32)
    #act3 = mx.symbol.Activation(data=fc3, name='relu3', act_type="relu")
    fc4 = mx.symbol.FullyConnected(data=act2, name='fc4', num_hidden=1)
    cost = mx.sym.LinearRegressionOutput(data=fc4, label=label)
    mod=mx.mod.Module(cost)
    return mod

def mxTrainer_deprecess(dirName,X_train,y_train,X_test,y_test,train_pair,test_pair):
    #print(X_train.shape)
    train_shape=X_train.tocsc().shape[0]
    test_shape=X_test.tocsc().shape[0]
    train_iter=mx.io.LibSVMIter(X_train,data_shape=train_shape,label=y_train,batch_size=100, last_batch_handle='discard')
    test_iter=mx.io.LibSVMIter(X_test,batch_size=100, last_batch_handle='discard')
    #train_iter = mx.io.NDArrayIter(X_train.toarray(),label=y_train,batch_size=100)
    #test_iter=mx.io.NDArrayIter(X_test.toarray(),batch_size=100)
    '''
    X = mx.sym.Variable('data')
    op = mx.symbol.Dropout(data=X, name='dp3', p=0.18)
    label= mx.sym.Variable(name='softmax_label')
    fc1= mx.sym.FullyConnected(data=op, num_hidden=128)
    act1 = mx.symbol.Activation(data=fc1, name='relu1', act_type="relu")
    fc2 = mx.symbol.FullyConnected(data=act1, name='fc2', num_hidden=64)
    act2 = mx.symbol.Activation(data=fc2, name='relu2', act_type="relu")
    fc3 = mx.symbol.FullyConnected(data=act2, name='fc3', num_hidden=32)
    act3 = mx.symbol.Activation(data=fc3, name='relu3', act_type="relu")
    fc4 = mx.symbol.FullyConnected(data=act3, name='fc4', num_hidden=1)
    cost = mx.sym.LinearRegressionOutput(data=fc4,label=label)#LogisticRegressionOutput(data=fc4, label=label)
    mod=mx.mod.Module.forward(symbol=cost,num_epoch=10,optimizer='sgd',)
    '''
    mod=rankNet()
    mod.bind(data_shapes=train_iter.provide_data,
             label_shapes=train_iter.provide_label)
    mod.fit(train_iter,num_epoch=10,optimizer="AdaGrad",eval_metric=mx.metric.TopKAccuracy(top_k=10))
    y_pred=mod.predict(test_iter)
    y_pred = y_pred.asnumpy().reshape(y_pred.shape[0])
    return y_pred

def mxTrainer(relationName,train,test,train_pair,test_pair):
    X_train, y_train, X_test, y_test = load_svmlight_files([train, test])
    X_train_col=X_train.shape[1]
    X_test_col=X_test.shape[1]
    col=max(X_test_col,X_train_col)
    train_iter=mx.io.LibSVMIter(data_libsvm=train,data_shape=(col,),batch_size=100)
    test_iter=mx.io.LibSVMIter(data_libsvm=test,data_shape=(col,),batch_size=100)
    print(test_iter)
    mod=rankNet()
    mod.bind(data_shapes=train_iter.provide_data,
             label_shapes=train_iter.provide_label)
    mod.fit(train_iter,num_epoch=5,optimizer="AdaGrad")
    y_pred=mod.predict(test_iter)
    print(relationName+str(y_pred.shape)+str(col))
    y_pred = y_pred.asnumpy().reshape(y_pred.shape[0])
    print(str(y_pred.shape)+str(y_test.shape))
    test_pair['score'] = y_pred
    print(roc_auc_score(y_true=y_test.reshape[y_test.shape[0]], y_score=y_pred))
    writeScoresInPraStyle(test_pair, train_pair, relationName)


def trainRelation(model,relationName):
    relation = os.path.join(path, relationName)
    train = relation + "/train.tsv"
    test = relation + "/test.tsv"
    train_pair = relation + "/trainPair.tsv"
    train_pair = pd.read_csv(train_pair, sep='\t', index_col=False, header=-1, names=['source', 'target', 'class'])
    train_pair = train_pair.to_csv(None, header=False, index=False).split('\n')
    test_pair = relation + "/testPair.tsv"
    test_pair = pd.read_csv(test_pair, sep='\t', index_col=False, header=-1, names=['source', 'target', "class"])
    #if(model=="mx"):
    #    mxTrainer(relationName,train=train,test=test,train_pair=train_pair,test_pair=test_pair)
    #    return
    #train_shape=pd.read_csv(train,sep=" ",header=-1,index_col=False).shape
    #test_shape=pd.read_csv(test,sep=" ",header=-1,index_col=False).shape
    X_train, y_train, X_test, y_test = load_svmlight_files([train, test])
    print(X_train.shape)
    r=int(y_train.shape[0])
    np.reshape(y_train,(r,1))
    r=int(y_test.shape[0])
    np.reshape(y_test,(r,1))
    if(model=="mx"):
        #train_iter=mx.io.LibSVMIter(data_libsvm=train,data_shape=(shape,),batch_size=10)
        X_train=mx.nd.sparse.array(X_train.astype("float32"))
        X_test=mx.nd.sparse.array(X_test.astype("float32"))
        train_iter = mx.io.NDArrayIter(X_train,label=y_train,batch_size=1, last_batch_handle='discard')
        test_iter=mx.io.NDArrayIter(X_test,batch_size=1, last_batch_handle='discard')
        #test_iter=mx.io.LibSVMIter(data_libsvm=test,data_shape=(shape,),batch_size=10)
        mod=rankNet()
        mod.bind(data_shapes=train_iter.provide_data,
             label_shapes=train_iter.provide_label)
        mod.fit(train_iter,num_epoch=5,optimizer="AdaGrad")
        y_pred=mod.predict(test_iter)
        print(str(y_test.shape)+"\t"+str(y_pred.shape))
        y_pred = y_pred.asnumpy().reshape(y_pred.shape[0])
        test_pair['score'] = y_pred
        print(roc_auc_score(y_true=y_test, y_score=y_pred))
        writeScoresInPraStyle(test_pair, train_pair, relationName)
    else:
        praRegression(model=model,dirName=relationName,X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,train_pair=train_pair,test_pair=test_pair)

for relation in os.listdir(path):
    os.mkdir(baseDir+relation)
    trainRelation(model,relation)
    #exit(0)