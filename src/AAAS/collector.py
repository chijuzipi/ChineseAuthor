'''
*********** This class to collect journal info from PNAS
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
    self.db = client.AAAS
    self.collection = self.db.PNAS_coll

    # read url list from txt
    with open("archive/processed/PNAS.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      time.sleep(2)
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]

      if "supp" in url or "Supp" in url:
        index += 1
        continue
      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, url, year)
      index += 1 
      print

  def parse(self, content, url, year):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    groups = soup.findAll("div", {"class" : "toc-level"})  
    for item in groups:
      article_type = item.find("h2")
      article_list = item.find("ul", {"class" : "cit-list"})
      if article_list is None:
        continue
      papers       = article_list.findAll("li", {"class":"cit"})
      
      if article_type is None:
        article_type = item.find("h3")
        if article_type is None:
          print url + " ---> " + "article_type is none"
          article_type = 'default'
        else:
          article_type = article_type.text 
      else:
        article_type = article_type.text 

      for paper in papers:
        title   = paper.find("h4", {"class" : "cit-title-group"})
        authors = paper.find("ul", {"class" : "cit-auth-list"})
        cite    = paper.find("cite")
        doi     = cite.find("span", {"class" : "cit-doi"})
        if title is None:
          title = "no-title"
        else:
          title = title.text

        if article_type == 'default':
          print title

        if doi is None:
          doi = "no-doi"
        else:
          doi = doi.text

        authortext = "no-author"
        if authors is not None:
          authortext = ""
          for author in authors.findAll("li"):
            authortext = authortext + " " + author.text
        else:
          print url + " ---> " + "author is none"
          print title
          continue
        
        
        comp = {}

        comp["title"]   = title
        comp["author"]  = authortext
        comp["doi"]     = doi
        comp["year"]    = year
        comp["type"] = article_type
        self.collection.insert(comp)
        '''
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
