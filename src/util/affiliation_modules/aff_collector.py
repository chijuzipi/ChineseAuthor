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
import re
  
from modules.Wiley import WileyParser
from modules.APS   import APSParser
from modules.ACS   import ACSParser

from modules.proxyLIB import URLlib2


class Collector:

  def __init__(self):
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    
    client = MongoClient()

    #TODO  set db
    self.db = client.ACS
    collection_list = self.db.collection_names(False)
    include_list = set()

    #TODO set collection
    include_list.add("JACS_coll")

    ## inclusive year range
    year_max = 2015
    year_min = 2005

    self.getAffi(collection_list, include_list, year_max, year_min)

  
  def getAffi(self, collection, include, year_max, year_min):
    for c in collection:
      if c in include:
        collection = self.db[c]
        cursor = collection.find()
        documents = list(cursor)
        index = 0 
        count = cursor.count()
        
        while index != count: 
          index = 1002
          doc       = documents[index]
          itemId    = doc['_id']
          year      = int(doc['year'])
          doi       = doc['doi']
          print doi
          break
          if year >= year_min and year <= year_max:

            # sleep 1 s
            #time.sleep(1)

            #TODO set module
            url = ACSParser.getUrl(c, doi)

            print "---> CRAWLING: " + url 
            print datetime.datetime.now()

            # timeout 60 s
            #TODO whether use proxy
            content = urllib2.urlopen(url, timeout=120).read()
            '''
            proxy = URLlib2()
            content = proxy.readURL(url)
            '''

            #TODO set function
            parser     = ACSParser(content)
            affi       = parser.getAffi()
            abstract   = parser.getAbs()
            #key        = parser.getKey()
            affi       = re.compile(r'[\n\r\t]').sub(' ', affi).rstrip()
            abstract   = re.compile(r'[\n\r\t]').sub(' ', abstract).rstrip()
            #key        = re.compile(r'[\n\r\t]').sub(' ', key).rstrip()
            #collection.update({'_id':itemId}, {"$set":{'affi': affi, 'abs':abstract}}, upsert=False)
            print len(affi)
            print len(abstract)
            #print key
            print "INDEX is " + str(index)
            
          index += 1
        cursor.close()


def main():
  collector = Collector()

if __name__ == '__main__':
    main()
