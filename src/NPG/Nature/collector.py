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
    with open("archive/processed/Nature2.txt") as f:
      pool = f.readlines()
   
    div = len(pool) / 20 
    index = 0
    
    #switch parse function
    blackList = set()

    '''
    blackList.add("http://www.nature.com/nature/journal/v428/n6978/index.html")
    blackList.add("http://www.nature.com/nature/journal/v428/n6979/index.html")
    blackList.add("http://www.nature.com/nature/journal/v423/n6940/index.html")
    blackList.add("http://www.nature.com/nature/journal/v424/n6948/index.html")
    blackList.add("http://www.nature.com/nature/journal/v423/n6939/index.html")
    '''

    while index < len(pool):
      infoArray = pool[index].split()
      url   = infoArray[0]
      year  = infoArray[1]
      divid = url.split('/')
      vol   = divid[5][1:]
      volNum = int(vol)
      if volNum > 424:
        index += 1
        continue
      
      if url in blackList:
        index += 1
        continue
      print "CRAWLING: " + url 
      print datetime.datetime.now()

      # tmeout 60 s
      content = urllib2.urlopen(url, timeout=500).read()
      self.parse1(content, url, year, f2)
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
        print typeText
        print titleText
        print authorText
        print doi
        print 

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
      #http://stackoverflow.com/questions/11647348/find-next-siblings-until-a-certain-one-using-beautifulsoup
      for index in range(len(article_titles)):
        title = article_titles[index].text
      
        author= article_authors[index].text
        doi   = article_dois[index].text

        title   = re.compile(r'[\n\r\t]').sub(' ', title)
        #desc    = re.compile(r'[\n\r\t]').sub(' ', desc)
        author  = re.compile(r'[\n\r\t]').sub(' ', author)
        doi     = re.compile(r'[\n\r\t]').sub(' ', doi)
        
        '''
        print "**************** Article ********************"
        print title
        print author
        print doi
        print
        '''

    for l_se in letter_sections:
      container = l_se.parent
      #container = a_se.find_parent('div', {'class':'container'})
      article_titles  = container.findAll('h4')
      article_authors = container.findAll('p', {"class":"aug"})
      article_dois    = container.findAll('p', {"class":"doi"})
      l1 = len(article_titles)
      l2 = len(article_authors)
      l3 = len(article_dois)
      if (l1 > 0 and l2 > 0 and l3 > 0 and not (l1 == l2 and l2 == l3 )):
        print "***************************NOT MATCH ARRAY *********************"
        print "***************************************************************************************************************************"
        continue
      for index in range(l1):
        title = article_titles[index].text
        author= article_authors[index].text

        if l3 > 0:
          doi   = article_dois[index].text
        else:
          doi   = ""

        title   = re.compile(r'[\n\r\t]').sub(' ', title)
        author  = re.compile(r'[\n\r\t]').sub(' ', author)
        doi     = re.compile(r'[\n\r\t]').sub(' ', doi)
        
        '''
        print "**************** Letter ********************"
        print title
        print author
        print doi
        print
        '''

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

        print "************* Article **************"
        print titleText
        print authorText
        print descText
        print

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
        
        print "************* Letter **************"
        print titleText
        print authorText
        print descText
        print 


def main():
  collector = Collector()

if __name__ == '__main__':
    main()
