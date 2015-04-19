'''
*********** This class to collect journal info from ACS 
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
    
    #open database
    client = MongoClient()
    self.db = client.ACS
    self.collection = self.db.test_coll
    
    # read url list from txt
    with open("archive/processed/AccountChem.txt") as f:
      pool = f.readlines()
    
    for url in pool:
      print url
      urlarray  = url.split() 
      url  = urlarray[0]
      year = urlarray[1]
      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, year)
    
## depracted ##
  def getAffi(self, doi):
    url = "http://pubs.acs.org/doi/full/" +  doi
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    out = soup.findAll("div", {"class" : "affiliations"})
    print "the affi is " + out[0].text
    return out[0].text 

  def parse(self, content, year):
    soup = BeautifulSoup(content)
    titleAndAuthor = soup.findAll("div", {"class" : "titleAndAuthor"})
    dates = soup.findAll("div", {"class" : "coverdate"})
    if len(dates) == 0:
      dates = soup.findAll("div", {"class": "epubdate"})
    DOIs  = soup.findAll("div", {"class" : "DOI"})
    
    if len(dates) == 0 | len(DOIs) == 0 | len(titleAndAuthor) == 0:
      return

    for i in range(len(titleAndAuthor)):
      comp = {}
      if len(titleAndAuthor[i]) < 2:
        continue
        
      title   = titleAndAuthor[i].contents[0].text
      author  = titleAndAuthor[i].contents[1].text 
      date    = dates[i].text
      date    = date.split(":")[1].strip()
      temp    = date.split("(")
      date    = temp[0]
      typ     = temp[1]
      doi     = DOIs[i].text
      doi     = doi.split(":")[1].strip()
      if(typ[len(typ)-1] == ')'):
        typ = typ[:len(typ)-1]

      comp["title"] = title
      comp["author"] = author 
      comp["date"] = date 
      comp["year"] = year
      comp["doi"] = doi 
      comp["type"] = typ 
      self.collection.insert(comp)
      print "save success " + comp["doi"]


def main():
  collector = Collector()

if __name__ == '__main__':
    main()
