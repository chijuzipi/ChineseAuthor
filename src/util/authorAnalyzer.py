'''
*********** This class to analyze chinese authorship from journals 
  (c) 2015 by Chad Zhou
  Northwestern University

  FUNCTION: Analyze the author's nationality by hashtable from mongoDB
**************************************************************************
'''

from pymongo import MongoClient
import re
from plotbar import Plot

class Analyzer:
  def __init__(self):
    # build hashmap
    self.firstname, self.surname = self.buildDict()
    '''
    name = "Anand Acharya"
    if self.isChinese(name):
      print "Loren M. Long is Chinese"
    '''

    client = MongoClient()
    db  = client.Wiley
    #db2 = client.ACS_processed
    collection = db.AdvMat_coll
    #self.collection2 = db2.joforganicchem_coll_chinese_first
    #self.collection3 = db2.joforganicchem_coll_chinese_co

    cursor    = collection.find({})
    documents = list(cursor)
    index     = 0
    count     = cursor.count()
    
    firstChinese = 0
    lastChinese  = 0
    self.count   = 0
    
    # total paper counter 
    totalResult = {}

    # chinese first author counter
    firstResult = {}

    # chinese co-author counter
    hasResult = {}

    # chinese correspondeing-author counter
    lastResult = {}
    
    while index != count: 
      if index % 1000 == 0:
        print "processed " + str(index) + " articles..."
      doc = documents[index]

      authors = doc['author']
      year    = doc["year"]

      authorList = self.getAuthors(authors)

      #increase total paper counter
      if year in totalResult:
        totalResult[year] += 1
      else:
        totalResult[year] = 1
      
      first, coauthor, last = self.detectChinese(authorList)
      
      if(first):
        self.collection2.insert(doc)
        self.collection3.insert(doc)
      elif(coauthor):
        self.collection3.insert(doc)

      index += 1

    cursor.close()
    
    self.alignment(totalResult, firstResult, hasResult, lastResult)
    #saveToDB(totalResult, firstResult, hasResult)    

    self.makeFigure(totalResult, firstResult, hasResult, lastResult)
    
  def makeFigure(self, total, first, has, last):
    yearList  = list(total.keys())
    yearList.sort()
    y1 = [] 
    y2 = []
    y3 = []
    y4 = []
    for year in yearList:
      y1.append(total[year])
      y2.append(first[year])
      y3.append(has[year])
      y4.append(last[year])

    plotHelper = Plot()
    plotHelper.plotBar(yearList, y1, y2, y3, y4, 'Adv. Mat.')

  def alignment(self, totalResult, firstResult, hasResult, lastResult):
    for key in totalResult:
      if key not in firstResult:
        firstResult[key] = 0
      if key not in hasResult:
        hasResult[key]   = 0
      if key not in lastResult:
        lastResult[key]   = 0

  def detectChinese(self, authorList):

    if self.isChinese(authorList[0]) and :
      return True, True

    for author in authorList:
      if self.isChinese(author):
        return False, True

    return False, False

  def isChinese(self, name):
    array = name.split()
    if len(array) == 0:
      return False
    sur   = array[len(array)-1] 
    first = array[0]
    if sur in self.surname and first in self.firstname:
      #self.count += 1
      return True
    else: 
      return False
      #print first + " " + sur
    
  def getAuthors(self, authors):
    out = re.split('and |, ', authors) 
    return out

  def buildDict(self):

    surnameSet = set() 
    firstSet   = set()
    f1 = open('../../library/firstname_handian.txt', 'r')
    f2 = open('../../library/surname_handian.txt', 'r')
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
