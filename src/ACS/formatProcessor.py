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
    self.db = client.author
    self.collection = self.db.JACS
    cursor = self.collection.find({})
    index = 0
    count = cursor.count()
    
    while index != count: 
      if index % 1000 == 0:
        print "processed " + str(index) + " articles..."
      doc       = cursor[index]
      itemId    = doc['_id']
      date      = doc['date']
      papertype = doc['type']
      
      templeng = len(papertype)
      if papertype[templeng-1] == ')':
        papertype = papertype[:templeng-1]

      year = self.getYear(date)
      self.collection.update({'_id':itemId}, {"$set":{'year':year, 'type':papertype}}, upsert=False)
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
