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
    self.db = client.APS
    collection_list = self.db.collection_names(False)
    include_list = set()
    include_list.add("prl_coll")
    for c in collection_list:
      if c in include_list:
        collection = self.db[c]
        cursor = collection.find()
        documents = list(cursor)
        index = 0 
        count = cursor.count()
        
        while index != count: 
          '''
          if index % 1000 == 0:
            print "processed " + c + str(index) + " articles..."
          '''
          doc       = documents[index]
          itemId    = doc['_id']
          #doi       = doc['doi']
          title     = doc['title']
          year      = doc['year']
          if year == "2014":
            collection.update({'_id':itemId}, {"$set":{'year': '1960'}}, upsert=False)
          if year == "1961":
            break

          '''
            
          title     = re.compile(r'[\n\r\t]').sub(' ', title)
          title     = title.rstrip()
          divid     = title.split()
          lastWord  = divid[len(divid)-1]
          if self.isPage(lastWord):
            print title
            divid = divid[:len(divid)-1]
            title = " ".join(divid)
            print title
            print
            
          if 'doi' in doc:
            doi       = doc['doi']
            if doi[:4] == 'doi:':
              doi = doi[4:]
          else:
            doi = ""
          author    = doc['author']
          author    = author.rstrip()
          partAuthor = author.split(',')
          authorText = ""
          for part in partAuthor:
            part = part.rstrip()
            if part != "":
              part = part.lower().title()
              authorText += part + ", "
          
          '''
          
          #collection.update({'_id':itemId}, {"$set":{'year': 1960}}, upsert=False)
          index += 1
        cursor.close()

  def isPage(self, word):
    if word[0] != 'p':
      return False
    for char in word[1:]:
      if char > '9' or char < '0':
        return False
    return True

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
