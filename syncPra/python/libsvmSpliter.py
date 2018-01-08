base = "/home/kdeapp/KBCompletion/Data/matrix_sfe/"
import os
import pandas as pd

for dir in os.listdir(base):
    relation = os.path.join(base, dir)
    # print(relation)
    train = relation + "/trainLibsvm.txt"
    test = relation + "/testLibsvm.txt"
    train = pd.read_csv(train, sep='\t', header=-1, names=['source', 'target', 'class', 'libsvm'],
                        dtype={'libsvm': object})
    test = pd.read_csv(test, sep='\t', header=-1, names=['source', 'target', 'class', 'libsvm'],
                       dtype={'libsvm': object})

    train=train.sort_values(["source"])
    train_group=train.groupby("source").size()
    test=test.sort_values(["source"])
    test_group=test.groupby("source").size()
    train_group.to_csv(relation + '/trainGroup.tsv', sep=',', header=False, index=False)
    test_group.to_csv(relation + '/testGroup.tsv', sep=',', header=False, index=False)
    # print(train.head())
    t1 = train[['source', 'target', 'class']]
    t1.to_csv(relation + '/trainPair.tsv', sep=',', header=False, index=True)
    train['libsvm'].to_csv(relation + '/train.tsv', header=False, index=False)
    t1 = test[['source', 'target', 'class']]
    t1.to_csv(relation + '/testPair.tsv', sep=',', header=False, index=True)
    test['libsvm'].to_csv(relation + '/test.tsv', header=False, index=False)