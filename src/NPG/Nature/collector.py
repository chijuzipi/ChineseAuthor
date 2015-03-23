'''
*********** This class to collect journal info from Nature
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
    self.db = client.NPG
    self.collection = self.db.Nature_coll
    '''

    f2 = open("log.txt", "w")
    # read url list from txt
    with open("archive/processed/Nature.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #switch parse function
    interval = set()
    interval.add("http://www.nature.com/nature/journal/v467/n7313/index.html")
    interval.add("http://www.nature.com/nature/journal/v387/n6636/index.html")
    moduleNum = 2 

    while index < len(pool):
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]
      divid = url.split("/")
      vol   = divid[5]
      if int(vol[1:]) > 386:
        index += 1
        continue
      
      
      if url in interval:
        moduleNum += 1
      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # tmeout 60 s
      content = urllib2.urlopen(url, timeout=500).read()
      if moduleNum == 0:
        self.parse1(content, url, year, f2)
        index += 1 
      elif moduleNum == 1:
        self.parse1(content, url, year, f2)
        index += 1 
      elif moduleNum == 2:
        self.parse2(content, url, year, f2)
        index += 100 

  def parse2(self, content, url, year,f2):
    print "using parse2"
    # first get all the possible info from url
    soup    = BeautifulSoup(content)
    trs     = soup.findAll('tr')
    
    typeText = ""
    for tr in trs:
      article_type = tr.find("a", {"name" : re.compile(".")})
      if article_type is not None:
        typeText = article_type.parent.find('b').text
        continue
      
      title      = tr.find('font', {'size' : '2'})
      if title is None:
        continue
      titleText = title.text
      authors    = tr.findAll('span', {'class' : 'author'})
      authorText = ""
      for author in authors:
        authorText += author.text + ", "

      doi      = tr.find('font', {'size' : '1'})
      if doi is None:
        doi = ""
      else:
        doi = doi.text.rstrip()
      
      typeText    = re.compile(r'[\n\r\t]').sub(' ', typeText)
      titleText   = re.compile(r'[\n\r\t]').sub(' ', titleText)
      authorText  = re.compile(r'[\n\r\t]').sub(' ', authorText)
      doi  = re.compile(r'[\n\r\t]').sub(' ', doi)
      print typeText
      print titleText
      print authorText
      print doi
      print 

    return

  def parse1(self, content, url, year,f2):
    print "using parse1"
    # first get all the possible info from url
    soup    = BeautifulSoup(content)
    '''
    section = soup.find("div", {"id" : "research"})  
    if section is None:
      #f2.write( "did not find group:--------------------> " + year + "\n")
      print "did not find group:--------------------> " + year
      return
    '''
    
    article_sections = soup.findAll("h3", {"id" : "af"})  
    if len(article_sections) == 0:
      article_sections = soup.findAll("h3", {"id" : "Article"})  
    letter_sections  = soup.findAll("h3", {"id" : "lt"})
    if len(letter_sections) == 0:
      letter_sections  = soup.findAll("h3", {"id" : "Letter"})
    for a_se in article_sections:
      #container = a_se.find_parent('div', {'class':'container'})
      articles  = a_se.parent.findAll('h4')
      f2.write(str(len(articles)) + " A" + "\n")
      print str(len(articles)) + " A" 
    for l_se in letter_sections:
      #container = a_se.find_parent('div', {'class':'container'})
      letters  = l_se.parent.findAll('h4')
      f2.write(str(len(letters)) + " L" + "\n")
      print str(len(letters)) + " L"

    '''
    subsections = section.findAll('section')
    print len(subsections)
    for subsection in subsections:
      div = section.find("div", {"id" : "af"})  
      if div is not None:
        articles = div.findAll('article')
        print str(len(articles)) + " articles"
      else:
        div = section.find("div", {"id" : "lt"})  
        if div is not None:
          articles = div.findAll('article')
          print str(len(articles)) + " letters"
    '''
      
    return

  def parse0(self, content, url, year,f2):
    # first get all the possible info from url
    soup    = BeautifulSoup(content)
    '''
    section = soup.find("div", {"id" : "research"})  
    if section is None:
      #f2.write( "did not find group:--------------------> " + year + "\n")
      print "did not find group:--------------------> " + year
      return
    '''
    
    article_sections = soup.findAll("div", {"id" : "af"})  
    letter_sections  = soup.findAll("div", {"id" : "lt"})
    for a_se in article_sections:
      articles = a_se.findAll('article')
      f2.write(str(len(articles)) + " A" + "\n")
      print str(len(articles)) + " A" 
    for l_se in letter_sections:
      letters  = l_se.findAll('article')
      f2.write(str(len(letters)) + " L" + "\n")
      print str(len(letters)) + " L"

    '''
    subsections = section.findAll('section')
    print len(subsections)
    for subsection in subsections:
      div = section.find("div", {"id" : "af"})  
      if div is not None:
        articles = div.findAll('article')
        print str(len(articles)) + " articles"
      else:
        div = section.find("div", {"id" : "lt"})  
        if div is not None:
          articles = div.findAll('article')
          print str(len(articles)) + " letters"
    '''
      
    return

        

def main():
  collector = Collector()

if __name__ == '__main__':
    main()
