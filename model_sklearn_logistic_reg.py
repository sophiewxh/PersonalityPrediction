import os
import numpy as np
from pprint import pprint
from sklearn import linear_model
from sklearn import svm
from util import TRAITS

'''
wifi by weekdays:
logistic reg
n fold:
79.4%
10 fold:
83.3%
svm:
n fold:
85.3%
10 fold:
85.8%
'''

def sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam):
    #clf = linear_model.LogisticRegression(C=lam, penalty='l2')
    clf = svm.SVC(C=lam, kernel='linear')
    
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc



def cross_validate(x, y, fold):
    lam_range = np.arange(0.001, 15.0, 0.01)
    lam_accs = []
    for lam in lam_range:
        accs = []
        for k in range(fold):
            #print 'fold: %d' % k
            hd_idx = np.arange(k, len(x), fold)
            x_test, y_test = x[hd_idx], y[hd_idx]
            x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
            #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mae')
            #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
            acc = sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam)
            accs.append(acc)
        avg_acc = np.mean(accs)
        #print "accuracy: %f " % avg_acc
        lam_accs.append(avg_acc)
    idx = np.argmax(lam_accs)
    best_lam = lam_range[idx]
    print "max accuracy: %f" % lam_accs[idx]
    print "best C: %f" % best_lam
        

    
if __name__ == '__main__':
    for trait in TRAITS:
        print '--------------'
        print trait
        fp = os.path.join('result', 'feature', 'all_features_fp_%s_cls_acii.csv' % trait)
        #fp = os.path.join('result', 'feature', 'all_features_fp_agrbl_cls_save.csv')
        #fp = os.path.join('result', 'feature', 'all_features_fp_agrbl_cls_sbp17.csv')
        data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
        #np.random.shuffle(data)
    
        x = data[:, 1:-1]
    
        y = data[:,-1]
    
        #cross_validate(x, y, fold=10)
        cross_validate(x, y, fold=len(x))
#     print np.sum(y) 
#     print len(y)
    