'''
*********** This class to analyze chinese authorship from journals 
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''

from pymongo import MongoClient
import re

class Analyzer:
  def __init__(self):
    # init hashmap
    self.firstname, self.surname = self.buildDict()

    client = MongoClient()
    db = client.author
    collection = db.JACS


    cursor = collection.find({})
    index = 0
    count = cursor.count()
    
    firstChinese = 0
    self.count = 0

    while index != count: 
      if index % 1000 == 0:
        print "processed " + str(index) + " articles..."
      doc = cursor[index]
      authors = doc['author']
      authorList = self.getAuthors(authors)
      self.analyze(authorList)
      index += 1
      cursor.close()
    print self.count

  def analyze(self, authorList):
    firstAuthor = authorList[0] 
    self.isChinese(firstAuthor)

  def isChinese(self, name):
    array = name.split()
    if len(array) == 0:
      return
    sur   = array[len(array)-1] 
    first = array[0]
    if sur in self.surname:
      self.count += 1
      #print first + " " + sur
    
  def getAuthors(self, authors):
    out = re.split('and |, ', authors) 
    return out

  def buildDict(self):

    surnameSet = set() 
    firstSet   = set()
    f1 = open('firstname.txt', 'r')
    f2 = open('surname.txt', 'r')
    firstname   = f1.readlines()
    surname     = f2.readlines()

    for item1 in firstname:
      firstSet.add(item1.rstrip('\n')) 
    for item2 in surname:
      surnameSet.add(item2.rstrip('\n').title()) 
    
    return firstSet, surnameSet

def main():
  analyzer = Analyzer()

if __name__ == '__main__':
  main()
