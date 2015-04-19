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
    data_train = self.getData('1980', '2015')

    print("Loading testing data......")
    data_test  = self.getSample()

    data_train_size_mb = self.size_mb(data_train['data'])
    data_test_size_mb = self.size_mb(data_test['data'])

    print("%d documents - %0.3fMB (training set)" % (
        len(data_train['data']), data_train_size_mb))

    print

    # split a training set and a test set
    y_train = data_train['target']


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
    feature_names = vectorizer.get_feature_names()

    if feature_names:
        feature_names = np.asarray(feature_names)


    # Train sparse Naive Bayes classifiers
    print('=' * 80)
    print("Using the Naive Bayes method to predict")
    clf = MultinomialNB(alpha=.01)
    #BernoulliNB(alpha=.01)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    for index in range(len(pred)):
      
      print "line 108", pred

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
    print "retrived chemistry papers: ", len(documents_chem)

    cursor = collection_phys.find({"year":{'$gte':lower, '$lt':upper}})
    documents_phys = list(cursor)
    print "retrived physics papers: ", len(documents_phys)

    cursor = collection_bio.find({"year":{'$gte':lower, '$lt':upper}})
    documents_bio = list(cursor)
    print "retrived bio papers: ", len(documents_bio)

    return self.build(documents_chem, documents_phys, documents_bio)

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

  def getSample(self):
    output = {}
    titles = []
    output['data'] = titles
    titles.append("Enhancement of proteasome activity by a small-molecule inhibitor of USP14")
    titles.append("Inhibition of follicular T-helper cells by CD8+ regulatory T cells is essential for self tolerance")
    titles.append("Molecular electronics: The single-molecule switch and transistor")
    titles.append("Phase transition enhanced thermoelectric figure-of-merit in copper chalcogenides")
    titles.append("Giant spontaneous Hall effect in zero-moment Mn2Ru x Ga")
    return output
     

  def size_mb(self, docs):
      return sum(len(s.encode('utf-8')) for s in docs) / 1e6

def main():
  classifier = Classifier()

if __name__ == '__main__':
    main()
