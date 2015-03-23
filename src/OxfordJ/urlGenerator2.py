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
    
    f1 = open("archive/processed/NAR.txt", 'w')
    with open("archive/NAResearch.txt") as f:
      pool = f.readlines()
    
    for url in pool:
      urlarray  = url.split() 
      url  = urlarray[0]
      year = urlarray[1]
      print "cralweling" + url
      # timeout 60 s
      content = urllib2.urlopen(url, timeout=120).read()
      soup = BeautifulSoup(content)
      htmls = soup.findAll(href=True)
      for html in htmls:
        urllink = html['href']
        if self.confirm(urllink):
          f1.write("http://nar.oxfordjournals.org"+urllink+ " " + year + "\n")

  def confirm(self, url):
    if "content" in url and "vol" in url and "issue" in url and "index.dtl" in url:
      return True
    else:
      return False


def main():
  collector = Collector()

if __name__ == '__main__':
    main()
