'''
*********** This class to collect journal info from Wiley
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
    self.db = client.Wiley
    self.collection = self.db.AdvFunMaterial_coll
    # read url list from txt
    with open("archive/processed/AdvFunMaterial.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      infoArray = pool[index].split()
      url = infoArray[0]
      year= infoArray[1]

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, url, year)
      index += 1 

  def parse(self, content, url, year):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    groups = soup.findAll("li", {"id" : re.compile('group*')})  
    for item in groups:
      heading = item.find('div', {'class' : 'subSectionHeading'})
      if(heading == None):
        sessionName = 'Default' 
      else:
        sessionName = heading.text 
        '''
      if len(heading) == 0:
        continue
        '''
      print '*** TYPE ***' + sessionName
      print
      articles = item.find('ol', {'class' : 'articles'}).findAll('li', recursive=False)
      if len(articles) == 0:
        continue
      for article in articles:
        comp = {}
        title   = article.find(href=True)
        doiarr  = title['href'].split('/')
        doi    = doiarr[2] + '/' + doiarr[3]
        sub     = article.findAll('p')
        if len(sub) < 2:
          continue
        authors = sub[0].text
        info    = sub[1].text

        if len(title) == 0 or len(doi) == 0 or len(authors) == 0:
          continue

        comp["title"]   = title.text
        comp["author"]  = authors
        comp["doi"]     = doi
        comp["info"]    = info
        comp["year"]    = year
        comp["article type"] = sessionName
        self.collection.insert(comp)
        print "save success " + comp["doi"]

        '''
        print '***TITLE*** ' + title.text
        print '***DOI*** ' + doi
        print '*** AUTHOR *** ' + authors
        print '*** INFO *** ' + info
        print year
        print
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
