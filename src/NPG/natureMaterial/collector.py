'''
*********** This class to collect journal info from NPG
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''

import urllib2, cookielib
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time, datetime
import re

class Collector:
  def __init__(self):
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    '''
    client = MongoClient()
    self.db = client.Wiley
    self.collection = self.db.testAdvFun
    '''
    # read url list from txt
    with open("../archive/processed/NatureMat.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      time.sleep(4)
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, url, year)
      index += div 

  def parse(self, content, url, year):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    groups = soup.findAll("div", {"class" : "subject"})  
    for item in groups:
      article_type = item.find("h3", {"class":"subject"})
      article_list = item.findAll("div", {"class" : "spacing"})
      
      if article_type is None:
        article_type = 'default'
      else:
        article_type = article_type.text 

      for paper in article_list:
        title   = paper.find("h4")
        authors = paper.find("p", {"class" : "aug"})
        doi     = paper.find("p", {"class" : "doi"})
        # Nature nano has the category attribute that put the article into fine categories.
        cata    = paper.find("p", {"class" : "category"})
        if title is None:
          title = "no-title"
        else:
          title = title.text

        if doi is None:
          doi = "no-doi"
        else:
          doi = doi.text

        if authors is None:
          authors = "no-author"
          continue
        else:
          authors = authors.text
        
        '''
        comp = {}

        comp["title"]   = title
        comp["author"]  = authortext
        comp["doi"]     = doi
        comp["year"]    = year
        comp["article type"] = article_type
        self.collection.insert(comp)
        print "save success " + comp["doi"]
        '''

        print '***TITLE*** ' + title
        print '***DOI*** ' + doi
        print '*** AUTHOR *** ' + authors
        print year
        print article_type
        print

  def getMap(self):
    out = {}
    year   = 1989 
    volume = 1
    while year <= 2015:
      out[str(volume)] = year
      volume += 1
      year += 1
    return out

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
