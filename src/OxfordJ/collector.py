'''
*********** This class to collect journal info from Oxford journal
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''
import urllib2, cookielib
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time, datetime

class Collector:
  def __init__(self):
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    client = MongoClient()
    self.db = client.Oxford
    self.collection = self.db.NAResearch_coll
    
    # read url list from txt
    with open("archive/processed/NAR2.txt") as f:
      pool = f.readlines()

    div = len(pool) / 20 
    index = 0

    while index < len(pool):
      time.sleep(2)
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]

      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 120 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, year)
      index += 1

  def parse(self, content, year):
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
          article_type = 'Default'
        else:
          article_type = article_type.text 
      else:
        article_type = article_type.text 

      article_type = article_type.lower().title()

      for paper in papers:
        title   = paper.find("h4", {"class" : "cit-title-group"})
        authors = paper.find("ul", {"class" : "cit-auth-list"})
        cite    = paper.find("cite")
        doi     = cite.find("span", {"class" : "cit-doi"})
        if title is None:
          title = ""
        else:
          title = title.text

        if article_type == 'default':
          print title

        if doi is None:
          doi = ""
        else:
          doi = doi.text
          doi = doi[5:]
          doi = doi.rstrip()

        authortext = ""
        if authors is not None:
          authortext = ""
          for author in authors.findAll("li"):
            authortext = authortext + " " + author.text
        else:
          continue
        
        comp = {}

        comp["title"]   = title
        comp["author"]  = authortext
        comp["doi"]     = doi
        comp["year"]    = year
        comp["type"] = article_type
        self.collection.insert(comp)
        print "save success " + comp["doi"]
        '''

        print '***TITLE*** ' + title
        print '***DOI*** ' + doi
        print '*** AUTHOR *** ' + authortext
        print year
        print article_type
        '''

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
