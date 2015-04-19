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
    
    client = MongoClient()
    self.db = client.NPG
    self.collection = self.db.Nature_coll

    f2 = open("log.txt", "w")
    # read url list from txt
    with open("archive/processed/Nature1.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 50
    index = 0
    

    while index < len(pool):
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]
      divid = url.split('/')
      vol   = divid[5][1:]
      volNum = int(vol)
      '''
      if volNum > 424:
        index += 1
        continue
      '''
      
      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # tmeout 60 s
      content = urllib2.urlopen(url, timeout=500).read()
      self.parse0(content, url, year, f2)
      index += 1 

  def parse2(self, content, url, year,f2):
    print "using parser 2"
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
      if typeText == 'Articles' or typeText == 'Article' or typeText == 'Letters':
        titleText = titleText.rstrip()
        parts     = titleText.split()
        titleText     = " ".join(parts[:len(parts)-1])
        print titleText
        '''
        print typeText
        print titleText
        print authorText
        print doi
        print 
        '''

        comp = {}

        comp["title"]   = titleText
        comp["author"]  = authorText
        comp["doi"]     = doi
        comp["year"]    = year
        comp["type"]    = typeText 
        self.collection.insert(comp)
        print "save success " + comp["doi"]

    return

  def parse1(self, content, url, year,f2):
    print "using parser 1"
    # first get all the possible info from url
    soup    = BeautifulSoup(content)
    
    article_sections = soup.findAll("h3", {"id" : "af"})  
    if len(article_sections) == 0:
      article_sections = soup.findAll("h3", {"id" : "Article"})  

    letter_sections  = soup.findAll("h3", {"id" : "lt"})
    if len(letter_sections) == 0:
      letter_sections  = soup.findAll("h3", {"id" : "Letter"})

    for a_se in article_sections:
      container = a_se.parent
      article_titles  = container.findAll('h4')
      for article in article_titles:
        nextNode = article
        title = article.text 
        author = ""
        doi = ""
        while True:
          nextNode   = nextNode.nextSibling
          if nextNode is None:
            break
          if nextNode.name == 'p':
            classValue = nextNode['class'][0]
            if classValue == 'aug':
              author = nextNode.text
            if classValue == 'doi':
              doi    = nextNode.text
          else:
            title   = re.compile(r'[\n\r\t]').sub(' ', title)
            author  = re.compile(r'[\n\r\t]').sub(' ', author)
            doi     = re.compile(r'[\n\r\t]').sub(' ', doi)
            '''
            print title
            print author
            print doi
            '''
            comp = {}

            comp["title"]   = title
            comp["author"]  = author
            comp["doi"]     = doi
            comp["year"]    = year
            comp["type"]    = "Article" 
            self.collection.insert(comp)
            print "save success " + comp["doi"]
            break

    for l_se in letter_sections:
      container = l_se.parent
      #container = a_se.find_parent('div', {'class':'container'})
      article_titles  = container.findAll('h4')
      for article in article_titles:
        nextNode = article
        title = article.text 
        author = ""
        doi = ""
        while True:
          nextNode   = nextNode.nextSibling
          if nextNode is None:
            break
          if nextNode.name == 'p':
            classValue = nextNode['class'][0]
            if classValue == 'aug':
              author = nextNode.text
            if classValue == 'doi':
              doi    = nextNode.text
          else:
            title   = re.compile(r'[\n\r\t]').sub(' ', title)
            author  = re.compile(r'[\n\r\t]').sub(' ', author)
            doi     = re.compile(r'[\n\r\t]').sub(' ', doi)
            '''
            print title
            print author
            print doi
            '''
            comp = {}

            comp["title"]   = title
            comp["author"]  = author
            comp["doi"]     = doi
            comp["year"]    = year
            comp["type"]    = "Letter" 
            self.collection.insert(comp)
            print "save success " + comp["doi"]
            break

  def parse0(self, content, url, year,f2):
    print "using parser 0"
    # first get all the possible info from url
    soup    = BeautifulSoup(content)
    
    article_sections = soup.findAll("div", {"id" : "af"})  
    letter_sections  = soup.findAll("div", {"id" : "lt"})
    for a_se in article_sections:
      articles = a_se.findAll('article')
      for article in articles:
        title = article.find('h1')
        if title is not None:
          titleText = title.text
        else:
          continue

        authors = article.find('ul', {'class':'authors'}).findAll('li')
        authorText = ""
        for author in authors:
          if author.find('li', {'class':'etal'}) is not None:
            continue
          authorText += author.text + ', '

        desc = article.find('p', {'class':'standfirst'})
        if desc is not None:
          descText = desc.text
        else:
          descText = ""

        titleText   = re.compile(r'[\n\r\t]').sub(' ', titleText)
        authorText  = re.compile(r'[\n\r\t]').sub(' ', authorText)
        descText  = re.compile(r'[\n\r\t]').sub(' ', descText)

        '''
        print "************* Article **************"
        print titleText
        print authorText
        print descText
        print
        '''
        comp = {}

        comp["title"]   = titleText
        comp["author"]  = authorText
        comp["desc"]    = descText 
        comp["year"]    = year
        comp["type"]    = "Article" 
        self.collection.insert(comp)
        print "save success " + comp["title"]

    for l_se in letter_sections:
      letters  = l_se.findAll('article')
      for letter in letters:
        title = letter.find('h1')
        if title is not None:
          titleText = title.text
        else:
          continue

        authors = letter.find('ul', {'class':'authors'}).findAll('li')
        authorText = ""
        for author in authors:
          if author.find('li', {'class':'etal'}) is not None:
            continue
          authorText += author.text + ', '

        desc = letter.find('p', {'class':'standfirst'})
        if desc is not None:
          descText = desc.text
        else:
          descText = ""

        titleText   = re.compile(r'[\n\r\t]').sub(' ', titleText)
        authorText  = re.compile(r'[\n\r\t]').sub(' ', authorText)
        descText  = re.compile(r'[\n\r\t]').sub(' ', descText)
        
        '''
        print "************* Letter **************"
        print titleText
        print authorText
        print descText
        print 
        '''
        comp = {}

        comp["title"]   = titleText
        comp["author"]  = authorText
        comp["desc"]    = descText 
        comp["year"]    = year
        comp["type"]    = "Letter" 
        self.collection.insert(comp)
        print "save success " + comp["title"]


def main():
  collector = Collector()

if __name__ == '__main__':
    main()
