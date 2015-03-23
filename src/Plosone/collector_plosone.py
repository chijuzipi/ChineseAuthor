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
    self.db = client.PLOS
    self.collection = self.db.PlosOne_coll

    # read url list from txt
    with open("archive/processed/plosone.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      url = pool[index]
      #issue = infoArray[2]

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      #self.parse(content, url, year, issue)
      self.parse(content, url)
      index += 1 

  def parse(self, content, url):
    # first get all the possible info from url
    soup   = BeautifulSoup(content)
    uppers  = soup.findAll("ul", {"id" : 'search-results'})  
    print len(uppers)
    for item in uppers:
      comp = {}
      title  = item.find('h2')
      if title is None:
        continue
      else:
        title = title.text

      authors = item.find('p', {'class' : 'authors'})
      if authors is None:
        continue
      else:
        authors = authors.text
      date    = item.find('p', {'class' : 'date'})
      if date is None:
        continue
      else:
        date = date.text
      parts   = date.split()
      year    = parts[len(parts)-1]
      actions = item.find('p', {'class' : 'actions'})
      if actions is None:
        continue
      else:
        doi     = actions.find('a')
        doi     = doi['data-doi'].split('/')
        doi     = doi[1]+'/'+doi[2]
      
      

      comp["title"]   = title
      comp["author"]  = authors
      comp["type"]    = "Articles"
      comp["doi"]     = doi
      #comp["issue"]   = issue
      comp["year"]    = year

      self.collection.insert(comp)
      print "save success " + comp["doi"]
      '''
      print '***TITLE*** ' + title
      print '***DOI*** ' + doi
      print '*** AUTHOR *** ' + authors
      print year
      print
      '''

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
