"""
==========================================================
Classification of scientific article using sparse features
==========================================================

This is an example showing how scikit-learn can be used to classify documents
by topics using a bag-of-words approach. This example uses a scipy.sparse
matrix to store the features and demonstrates various classifiers that can
efficiently handle sparse matrices.

The dataset used in this example is the 20 newsgroups dataset. It will be
automatically downloaded, then cached.

The bar plot indicates the accuracy, training time (normalized) and test time
(normalized) of each classifier.

"""

# Original Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Olivier Grisel <olivier.grisel@ensta.org>
#         Mathieu Blondel <mathieu@mblondel.org>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
# Revise Author: Chad Zhou <chadzhoubrother@gmail.com>
  
import logging
import numpy as np
import sys
from time import time
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics

from pymongo import MongoClient

class Classifier:

  def __init__(self):
    # target (1, 2, 3,....)
    global y_train
    global y_test

    # title ("shape selective of anisotropic nanoparticle ....")
    global X_train
    global X_test

    print("Loading training data......")
    data_train = self.getData('2000', '2010')
    print "lenth of data_train", len(data_train)

    print("Loading testing data......")
    data_test  = self.getData('2010', '2011')
    print "lenth of data_test", len(data_test)

    data_train_size_mb = self.size_mb(data_train['data'])
    data_test_size_mb = self.size_mb(data_test['data'])

    print("%d documents - %0.3fMB (training set)" % (
        len(data_train['data']), data_train_size_mb))
    print("%d documents - %0.3fMB (test set)" % (
        len(data_test['data']), data_test_size_mb))
    print()

    # split a training set and a test set
    y_train, y_test = data_train['target'], data_test['target']


    ''' ############# Using hashing to do transform the data ################
    vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
                                   n_features=opts.n_features)
    X_train = vectorizer.transform(data_train.data)
    '''
    # default using TF-IDF transformation
    print("Extracting features from the training data using a sparse vectorizer...")
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
    X_train = vectorizer.fit_transform(data_train['data'])

    print("Extracting features from the test data using the same vectorizer...")
    X_test = vectorizer.transform(data_test['data'])

    # mapping from integer feature name to original token string
    '''
    if opts.use_hashing:
        feature_names = None
    else:
        feature_names = vectorizer.get_feature_names()
    '''
    feature_names = vectorizer.get_feature_names()

    if feature_names:
        feature_names = np.asarray(feature_names)

    results = []

    # Train sparse Naive Bayes classifiers
    print('=' * 80)
    print("Using the Naive Bayes method")
    results.append(self.benchmark(MultinomialNB(alpha=.01)))
    results.append(self.benchmark(BernoulliNB(alpha=.01)))

    for clf, name in (
            (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
            (Perceptron(n_iter=50), "Perceptron"),
            (PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive")):
            #(KNeighborsClassifier(n_neighbors=10), "kNN")):
            #(RandomForestClassifier(n_estimators=100), "Random forest")):
        print('=' * 80)
        print(name)
        results.append(self.benchmark(clf))
    for penalty in ["l2", "l1"]:
        print('=' * 80)
        print("%s penalty" % penalty.upper())
        # Train Liblinear model
        results.append(self.benchmark(LinearSVC(loss='l2', penalty=penalty,
                                                dual=False, tol=1e-3)))

        # Train SGD model
        results.append(self.benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                               penalty=penalty)))

    # Train SGD with Elastic Net penalty
    print('=' * 80)
    print("Elastic-Net penalty")
    results.append(self.benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                           penalty="elasticnet")))

    # Train NearestCentroid without threshold
    print('=' * 80)
    print("NearestCentroid (aka Rocchio classifier)")
    results.append(self.benchmark(NearestCentroid()))

    
    print('=' * 80)
    print("LinearSVC with L1-based feature selection")
    # The smaller C, the stronger the regularization.
    # The more regularization, the more sparsity.
    results.append(self.benchmark(Pipeline([
      ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3)),
      ('classification', LinearSVC())
    ])))

    '''
    # make some plots
    indices = np.arange(len(results))

    results = [[x[i] for x in results] for i in range(4)]

    clf_names, score, training_time, test_time = results
    training_time = np.array(training_time) / np.max(training_time)
    test_time = np.array(test_time) / np.max(test_time)

    plt.figure(figsize=(12, 8))
    plt.title("Score")
    plt.barh(indices, score, .2, label="score", color='r')
    plt.barh(indices + .3, training_time, .2, label="training time", color='g')
    plt.barh(indices + .6, test_time, .2, label="test time", color='b')
    plt.yticks(())
    plt.legend(loc='best')
    plt.subplots_adjust(left=.25)
    plt.subplots_adjust(top=.95)
    plt.subplots_adjust(bottom=.05)

    for i, c in zip(indices, clf_names):
        plt.text(-.3, i, c)

    plt.show()
    '''
    ###############################################################################
    # Benchmark classifiers
  def benchmark(self, clf):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    print pred

    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)

    if hasattr(clf, 'coef_'):
        print("dimensionality: %d" % clf.coef_.shape[1])
        print("density: %f" % density(clf.coef_))

    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time

  def getData(self, lower, upper):
    client = MongoClient()
    db_chem = client.ACS
    db_phys = client.APS
    db_bio  = client.Cell

    collection_chem = db_chem['JACS_coll']
    collection_phys = db_phys['prl_coll']
    collection_bio  = db_bio['Cell_coll']
    
    print lower," ",  upper
    cursor = collection_chem.find({"year":{'$gte':lower, '$lt':upper}})
    documents_chem = list(cursor)
    print "the original doc length: ", len(documents_chem)

    cursor = collection_phys.find({"year":{'$gte':lower, '$lt':upper}})
    documents_phys = list(cursor)
    print len(documents_phys)

    cursor = collection_bio.find({"year":{'$gte':lower, '$lt':upper}})
    documents_bio = list(cursor)
    print len(documents_bio)

    return self.build(documents_chem, documents_phys, documents_bio)
    #return [], [], [] 


  def build(self, chem, phys, bio):
    # process the lists of documents
    for doc in chem:
      doc['target'] = 0
      doc['target_name'] = "chemistry"
    for doc in phys:
      doc['target'] = 1
      doc['target_name'] = "physics"
    for doc in bio:
      doc['target'] = 2
      doc['target_name'] = "biology"

    overall = chem + phys + bio

    output  = {}
    output['data'] = []
    output['target_names'] = []
    output['target']  = []
    output['year']    = []

    index = 0 
    count = len(overall) 

    while index != count: 
      '''
      if index % 1000 == 0 and index > 0:
        print "loaded " + str(index) + " articles..."
      '''
      doc       = overall[index]
      title     = doc['title']
      year      = doc['year']
      target    = doc['target']
      target_name    = doc['target_name']
      output['data'].append(title)
      output['target'].append(target)
      output['target_names'].append(target_name)
      output['year'].append(year)
      index += 1

    return output

  def size_mb(self, docs):
      return sum(len(s.encode('utf-8')) for s in docs) / 1e6

def main():
  classifier = Classifier()

if __name__ == '__main__':
    main()
