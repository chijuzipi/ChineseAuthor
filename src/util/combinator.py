'''
**************************************************************************
  (c) 2015 by Chad Zhou
  Northwestern University

  FUNCTION: This conbinator is to combine each collections in different database in to a single db (ALL)

**************************************************************************
'''
from pymongo import MongoClient
import re

class Collector:
  def __init__(self):
    client = MongoClient()
    publishers = set()
    '''
    publishers.add("AAAS")
    publishers.add("ACS")
    publishers.add("APS")
    publishers.add("Cell")
    publishers.add("Science")
    publishers.add("Wiley")
    publishers.add("NPG")
    '''
    publishers.add("Oxford")
    db2 = client.ALL
    collection2 = db2.all_jour_coll
    for publisher in publishers:
      db1 = client[publisher]
      collection_list = db1.collection_names(False)
      '''
      process_list = set()
      process_list.add("Nature_coll")
      for c in process_list:
      '''
      for c in collection_list:
        collection1 = db1[c]
        journal = c.split("_")[0]
        cursor = collection1.find()
        documents = list(cursor)
        index = 0 
        count = cursor.count()
        
        while index != count: 
          if index % 1000 == 0:
            print "processed " + journal + " " + str(index) + " articles..."
          doc = documents[index]
          
          doc['journal'] = journal
          doc['publisher'] = publisher 
          collection2.insert(doc)
          index += 1
        cursor.close()

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
