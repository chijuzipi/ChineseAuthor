# for Arxiv 
import urllib2, cookielib
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time, datetime
import re

class URLGenerator:
  def __init__(self):
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    # when the urls from file
    #self.generate()

    # when the urls can be direct synthesized
    self.synthesis()

  def generate(self):
    f1 = open('archive/processed/a.txt', 'r')
    f2 = open('archive/processed/prl_processed.txt', 'w')
    urls = f1.readlines()
    for line in urls:
      line = line.split()
      url  = line[0]
      vol  = line[1]

      content = urllib2.urlopen(url, timeout=120).read()
      soup    = BeautifulSoup(content)
      token   = str("v" + vol)
      link    = soup.find("h4", {"id": token})
      year    = link.find("small").text
      year    = year.split()
      year    = year[len(year)-1]
      print url
      lists = link.findNext('ul').findAll("li")
      parent = "http://journals.aps.org"
      for item in lists:
        href = item.find(href=True) 
        hreflink = href["href"]
        f2.write(parent + hreflink+ " " + year + '\n')


  def getYear(self, itemid):
    return itemid.split('_')[1]

  def synthesis(self):
    f = open('archive/processed/highEnergyExper.txt', 'w')
    parentURL = "http://arxiv.org/list/hep-ex/"
    for vol in range (94,100):
      for issue in range (1, 13):
        if len(str(vol)) == 1:
          vol = "0"+str(vol)
        if len(str(issue)) == 1:
          issue = "0"+str(issue)
        url  = parentURL + str(vol) + str(issue)+"?show=2000"
        year = "19" + str(vol)
        #print url
        f.write(url +" " + year + '\n')
    for vol in range (0,16):
      for issue in range (1, 13):
        if len(str(vol)) == 1:
          vol = "0"+str(vol)
        if len(str(issue)) == 1:
          issue = "0"+str(issue)
        url  = parentURL + str(vol) + str(issue)+"?show=2000"
        year = "20" + str(vol)
        #print url
        f.write(url +" " + year + '\n')
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

