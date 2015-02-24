'''
*********** This class to collect journal info from APS
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
    self.db = client.AAAS
    self.collection = self.db.PNAS_coll
    '''

    # read url list from txt
    with open("archive/processed/prb_processed.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, url, year)
      index += div
      print

  def parse(self, content, url, year):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    papers = soup.findAll('div',{'class': lambda x: x and re.search('article(\s|$)', x)})
    for paper in papers:
      title   = paper.find("h5", {"class" : "title"})
      authors = paper.find("h6", {"class" : "authors"})
      doi     = paper["data-id"]
      #doi     = cite.find("span", {"class" : "cit-doi"})
      if title is None:
        title = "no-title"
      else:
        title = title.text


      if authors is None:
        authors = "no author"
      else:
        authors = authors.text
      
      print title
      print authors
      print doi
      '''
      comp = {}

      comp["title"]   = title
      comp["author"]  = authortext
      comp["doi"]     = doi
      comp["year"]    = year
      comp["type"] = article_type
      self.collection.insert(comp)
      print "save success " + comp["doi"]

      print '***TITLE*** ' + title
      print '***DOI*** ' + doi
      print '*** AUTHOR *** ' + authortext
      print year
      print article_type
      '''

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
