'''
*********** This class to collect journal info from arxiv
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
    self.db = client.arxiv
    self.collection = self.db.hepex_coll

    # read url list from txt
    with open("archive/processed/highEnergyExper.txt") as f:
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
      index += 1
      print

  def parse(self, content, url, year):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    papers = soup.findAll("div", {"class":"meta"})
    for paper in papers:
      title   = paper.find("div", {"class" : "list-title"})
      authors = paper.find("div", {"class" : "list-authors"})
      subject = paper.find("div", {"class" : "list-subjects"})
      if title is None:
        title = "no-title"
      else:
        title = title.text

      if authors is None:
        authors = "no-author"
      else:
        authors = authors.text

      if subject is None:
        subject = "no-subject"
      else:
        subject = subject.text

      title     = title.split(":")[1].strip()
      title     = re.compile(r'[\n\r\t]').sub(' ', title)
      authors   = authors.split(":")[1].strip().rstrip('\n')
      authors   = re.compile(r'[\n\r\t]').sub(' ', authors)
      subject   = subject.split(":")[1].strip().rstrip('\n')
      subject   = re.compile(r'[\n\r\t]').sub(' ', subject)
      
      
      comp = {}

      comp["title"]   = title
      comp["author"]  = authors
      comp["subject"]     = subject 
      comp["year"]    = year
      self.collection.insert(comp)
      print "save success "

      '''
      print year
      print '***TITLE*** ' + title
      print '*** AUTHOR *** ' + authors
      print '*** SUBJECT *** ' + subject
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
