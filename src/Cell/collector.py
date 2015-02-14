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

    '''
    client = MongoClient()
    self.db = client.Wiley
    self.collection = self.db.testAdvFun
    '''
    # read url list from txt
    with open("archive/processed/Cell.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]
      issue = infoArray[2]
      if(issue == 'Supplement'):
        continue

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, url, year, issue)
      index += div 

  def parse(self, content, url, year, issue):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    groups = soup.findAll("div", {"class" : 'articleCitation'})  
    for item in groups:
      comp = {}
      info   = item.find('div', {'class' : 'detail'})
      title  = info.find('div', {'class' : 'title'}).text
      authors = info.find('div', {'class' : 'authors'}).text
      doi    = info.find('div', {'class' : 'doi'}).text
      print

      '''
      comp["title"]   = title.text
      comp["author"]  = authors
      comp["doi"]     = doi
      comp["info"]    = info
      comp["year"]    = year
      comp["article type"] = sessionName
      self.collection.insert(comp)
      print "save success " + comp["doi"]
      '''

      print '***TITLE*** ' + title
      print '***DOI*** ' + doi
      print '*** AUTHOR *** ' + authors
      print '*** ISSUE *** ' + issue
      print year
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
