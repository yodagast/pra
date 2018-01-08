import tensorflow as tf
import numpy as np
import mxnet as mx
def convert_sparse_matrix_to_sparse_tensor(X):
    coo = X.tocoo()
    indices = np.mat([coo.row, coo.col]).transpose()
    return tf.SparseTensor(indices, coo.data, coo.shape)

def trainer(dirName,X_train,y_train,X_test,y_test,train_pair,test_pair):
    train_iter = mx.io.NDArrayIter(X_train,label=y_train, batch_size=100)
    test_iter=mx.io.NDArrayIter(X_train)
    data = mx.sym.var('data')
    fc1 = mx.sym.FullyConnected(data, num_hidden=128)
    act1 = mx.sym.Activation(fc1, act_type="relu")
    fc2=mx.sym.FullyConnected(act1, num_hidden=10)
    loss = mx.sym.SoftmaxOutput(fc2)
    mod = mx.mod.Module(loss)
    mod.fit(train_iter)
    y_pred=mod.predict(test_iter,batch_size=10)
    print(y_pred)
    #writeScoresInPraStyle(test_pair, train_pair, dirName)

