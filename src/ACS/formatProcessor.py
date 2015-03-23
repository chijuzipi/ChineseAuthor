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
    self.db = client.AAAS
    self.collection = self.db.PNAS_coll
    cursor = self.collection.find({})
    index = 0 
    count = cursor.count()
    
    while index != count: 
      if index % 1000 == 0:
        print "processed " + str(index) + " articles..."
      doc       = cursor[index]
      itemId    = doc['_id']
      #title     = doc['title']
      doi       = doc['doi']
      if len(doi) < 1: 
        doi = "" 
      else:
        doi       = "1"+doi
      ''' 
      templeng = len(papertype)
      if templeng == 0:
        papertype = "Article"
      elif papertype[templeng-1] == ')':
        papertype = papertype[:templeng-1]

      year = self.getYear(date)
      '''

      self.collection.update({'_id':itemId}, {"$set":{'doi':doi}}, upsert=False)
      #print year
      index += 1
      cursor.close()

  def getYear(self, date):
    out = date.split(',')
    if len(out) < 2:
      year = out[0].split() 
      print year[1].strip()
      return year[1].strip()
    return out[1].strip()

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
