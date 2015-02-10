'''
*********** This class to analyze chinese authorship from journals 
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''

from pymongo import MongoClient
import re
from plotbar import Plot

class Analyzer:
  def __init__(self):
    # build hashmap
    self.firstname, self.surname = self.buildDict()

    client = MongoClient()
    db = client.author
    collection = db.AcsNano

    cursor = collection.find({})
    index = 0
    count = cursor.count()
    
    firstChinese = 0
    self.count = 0
    
    # total paper counter 
    totalResult = {}

    # chinese first author counter
    firstResult = {}

    # chinese co-author counter
    hasResult = {}
    
    while index != count: 
      if index % 1000 == 0:
        print "processed " + str(index) + " articles..."
      doc = cursor[index]

      authors = doc['author']
      date    = doc['date']

      authorList = self.getAuthors(authors)
      year = self.getYear(date)

      #increase total paper counter
      if year in totalResult:
        totalResult[year] += 1
      else:
        totalResult[year] = 1
      
      first, coauthor = self.detectChinese(authorList)

      if(first):
        if year in firstResult:
          firstResult[year] += 1
        else:
          firstResult[year]  = 1
      if(coauthor):
        if year in hasResult:
          hasResult[year] += 1
        else:
          hasResult[year]  = 1

      index += 1
      cursor.close()
    
    self.alignment(totalResult, firstResult, hasResult)
    #saveToDB(totalResult, firstResult, hasResult)    

    self.makeFigure(totalResult, firstResult, hasResult)
    
  def makeFigure(self, total, first, has):
    yearList  = list(total.keys())
    yearList.sort()
    y1 = [] 
    y2 = []
    y3 = []
    for year in yearList:
      y1.append(total[year])
      y2.append(first[year])
      y3.append(has[year])

    plotHelper = Plot()
    plotHelper.plotBar(yearList, y1, y2, y3, 'JACS')

  def alignment(self, totalResult, firstResult, hasResult):
    for key in totalResult:
      if key not in firstResult:
        firstResult[key] = 0
      if key not in hasResult:
        hasResult[key]   = 0

  def getYear(self, date):
    out = date.split(',')
    if len(out) < 2:
      print date
      return out[0].strip()

    return out[1].strip()

  def detectChinese(self, authorList):

    if self.isChinese(authorList[0]):
      return True, True

    for author in authorList:
      if self.isChinese(author):
        return False, True

    return False, False

  def isChinese(self, name):
    array = name.split()
    if len(array) == 0:
      return
    sur   = array[len(array)-1] 
    first = array[0]
    if sur in self.surname:
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
    f1 = open('../library/firstname_handian.txt', 'r')
    f2 = open('../library/surname_handian.txt', 'r')
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
