'''
*********** This class to collect journal info from ACS 
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''
from pymongo import MongoClient
import re

class Collector:
  def __init__(self):
    
    client = MongoClient()
    self.db = client.Oxford
    collection_list = self.db.collection_names(False)
    exclude_list = set()
    for c in collection_list:
      if c not in exclude_list:
        collection = self.db[c]
        cursor = collection.find()
        documents = list(cursor)
        index = 0 
        count = cursor.count()
        
        while index != count: 
          if index % 1000 == 0:
            print "processed " + c + str(index) + " articles..."
          doc       = documents[index]
          itemId    = doc['_id']
          #doi       = doc['doi']
          title     = doc['title']
          title     = re.compile(r'[\n\r\t]').sub(' ', title)
          title     = title.rstrip()
          author    = doc['author']
          author    = author.rstrip()
          
          collection.update({'_id':itemId}, {"$set":{'author':author}}, upsert=False)
          index += 1
        cursor.close()

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
