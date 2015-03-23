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
    opener = urllib2.build_opener()
    cookie = {}
    cookie['is_returning']='1'
    cookie['OAX']='fD63+FUMyCcAAaRV'
    cookie['JSESSIONID']='ec2s3ho50q5g1.x-aip-live-03'
    cookie['_ga']='GA1.2.1147096743.1426901033'
    opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookie.items())))
    f = opener.open("http://scitation.aip.org/content/aip/journal/apl/105/4?pageSize=10000&page=1").read()
    f2 = open("test.html", "w")
    f2.write(f)
    return
    
  
    '''
    client = MongoClient()
    self.db = client.AIP
    self.collection = self.db.APL_coll
    '''

    # read url list from txt
    with open("archive/processed/APL2.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #yearMap = self.getMap() 

    while index < len(pool):
      time.sleep(2)
      infoArray = pool[index].split()
      urll   = infoArray[0]
      #urll   = urll + "?pageSize=10000&page=1"
      year  = infoArray[1]

      print "CRAWLING: " + urll
      print datetime.datetime.now()
     
      '''
      headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201Firefox/3.5.6', 
      'Cookie':'is_returning=1;OAX=fD63+FUMyCcAAaRV;JSESSIONID=ec2s3ho50q5g1.x-aip-live-03;_gat_UA-39337252-1=1;_ga=GA1.2.1147096743.1426901033'}
      req = urllib2.Request(
        url = urll,
        headers = headers
      )
      '''

      # timeout 60 s
      content = urllib2.urlopen(req, timeout=120).read()
      f2 = open("test.html", "w")
      f2.write(content)
      return
      self.parse(content, year)
      index += div 
      print

  def parse(self, content, year):
    # first get all the possible info from url
    soup = BeautifulSoup(content)
    container = soup.findAll("div", {"class" : "issueTocContents"})  
    print len(container)
    return
    groups    = container.findAll("ul", {"class":"flat"})
    for item in groups:
      article_type = item.find("li", {"class" : "issueToShowhide"})
      article_list = item.find("li", {"class" : "sectionContents"})
      if article_list is None:
        continue
      papers       = article_list.findAll("div", {"class":"articleInToc"})
      
      if article_type is None:
        article_type = item.find("h3")
        if article_type is None:
          print url + " ---> " + "article_type is none"
          article_type = 'Default'
        else:
          article_type = article_type.text 
      else:
        article_type = article_type.text 

      for paper in papers:
        title     = paper.find("h5")
        authors   = paper.find("div", {"class" : "authorsWithPopup"})
        source    = paper.find("div", {"class" : "articleSourceTag"})
        doiLink   = source.find("a", {"class" : "externallink"})

        if title is None:
          title = ""
        else:
          title = title.text

        if doiLink is None:
          doiLink = ""
        else:
          doiLink = doiLink.text
        divid = doiLink.split("/")
        doi   = divid[3]+divid[4]

        authortext = ""
        if authors is not None:
          authortext = ""
          for author in authors.findAll("a"):
            authortext = authortext + " " + author.text
        else:
          print url + " ---> " + "author is none"
          print title
          continue

        authortext = authortext.rstrip()

        '''
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
