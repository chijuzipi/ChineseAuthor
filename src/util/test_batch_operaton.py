'''
*********** This conbinator is to combine each collections in different database in to a single db 
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''
from pymongo import MongoClient
import re

class Collector:
  def __init__(self):
    publishers = set() 
    publishers.add("Wiley")
    publishers.add("ACS")
    publishers.add("APS")

    client = MongoClient()
    for publisher in publishers:
      self.db1 = client[publisher]
      collection_list = self.db1.collection_names(False)
      for c in collection_list:
        print c

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
