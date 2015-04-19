import logging
import numpy as np
from optparse import OptionParser
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


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


# parse commandline arguments

###############################################################################
# Load some categories from the training set
categories = [
  'alt.atheism',
  'talk.religion.misc',
  'comp.graphics',
  'sci.space',
]

remove = ('headers', 'footers', 'quotes')

print("Loading 20 newsgroups dataset for categories:")
print(categories if categories else "all")

data_train = fetch_20newsgroups(subset='test', categories=categories,
                                shuffle=True, random_state=42,
                                remove=remove)

'''
data_test = fetch_20newsgroups(subset='test', categories=categories,
                               shuffle=True, random_state=42,
                               remove=remove)
'''
print type(data_train)
print ('data loaded')
print data_train.keys()
#print len(data_train.data)
for index in range(800, 850):
  #print data_train.data[index]
  print "target is " , data_train.target[index] 
  print "target name is ", data_train.target_names[data_train.target[index]]
  print data_train.filenames[index]
  print data_train.DESCR
