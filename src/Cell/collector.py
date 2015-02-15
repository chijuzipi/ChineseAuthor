'''
*********** This class to collect journal info from Cell 
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
    client = MongoClient()
    self.db = client.Cell
    self.collection = self.db.Cell_coll

    # read url list from txt
    with open("archive/processed/Cell.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 4 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]
      issue = infoArray[2]
      if(issue == 'Supplement'):
        index += 1
        continue

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, url, year, issue)
      index += 1

  def parse(self, content, url, year, issue):
    # first get all the possible info from url
    soup   = BeautifulSoup(content)
    uppers  = soup.findAll("div", {"class" : 'articleCitations'})  
    for upper in uppers:
      groups = upper.findAll("div", {"class" : ['heading', 'articleCitation']})  
      if(len(groups) == 0):
        continue
      article_type = ""
      for item in groups:
        #print item.text
        if 'heading' in item['class']:
          article_type = item.text 
          print "----------------->>>", item.text
          continue
          
        comp = {}
        info   = item.find('div', {'class' : 'detail'})
        title  = info.find('div', {'class' : 'title'}).text
        authors = info.find('div', {'class' : 'authors'}).text
        doi    = info.find('div', {'class' : 'doi'}).text

        if article_type == "":
          article_type = "Articles"

        comp["title"]   = title
        comp["author"]  = authors
        comp["type"]    = article_type
        comp["doi"]     = doi
        comp["issue"]   = issue
        comp["year"]    = year

        self.collection.insert(comp)
        print "save success " + comp["doi"]
        '''
        print '***TYPE*** ' + article_type 
        print '***TITLE*** ' + title
        print '***DOI*** ' + doi
        print '*** AUTHOR *** ' + authors
        print '*** ISSUE *** ' + issue
        print year
        print
        '''

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
