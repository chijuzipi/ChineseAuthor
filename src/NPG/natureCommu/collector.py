# the term attribute cannot be accessed for now
'''
*********** This class to collect journal info from Nature Communication
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''

import urllib2, cookielib
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time, datetime
import re
import string

class Collector:
  def __init__(self):
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    '''
    client = MongoClient()
    self.db = client.NPG
    self.collection = self.db.NatureChemistry_coll
    '''

    # read url list from txt
    with open("../archive/processed/NatureCommu2.txt") as f:
      pool = f.readlines()
    
    div = len(pool) / 20 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      #time.sleep(2)
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]
      
      url = "http://www.nature.com/ncomms/archive/date/2011/10/index.html"

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 120 s

      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, url, year)
      index += div

      return

  def parse(self, content, url, year):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    articles = soup.findAll("li", {"class":"article"})
    print "here at line 53 is : " + str(len(articles))

    for article in articles:
      title   = article.find("h3", {"class":"title"})
      authors = article.find("dd", {"class":"authors"})
      #terms   = article.findAll("dt", {"class":"hidden"})
    

      if title is None:
        title = "no-title"
      else:
        title = title.text

      if authors is None:
        continue
      else:
        authors = authors.text
        authors = re.compile(r'[\n\r\t]').sub(' ', authors)
      
      '''
      if terms is not None:
        print terms.text
        continue
        terms = terms.findAll("li")
        termtext = ""
        for term in terms:
          termtext += term.text + "|"
      else:
        termtext = "no-term"
        print termtext
        continue
      
      comp = {}

      comp["title"]   = title
      comp["author"]  = authors
      comp["doi"]     = doi
      comp["year"]    = year
      comp["type"] = article_type
      self.collection.insert(comp)
      print "save success " + comp["doi"]
      '''

      print '***TITLE*** ' + title
      print '*** AUTHOR *** ' + authors
      #print '*** TERM *** ' + termtext 
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
