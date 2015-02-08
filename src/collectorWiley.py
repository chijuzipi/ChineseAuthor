import urllib2, cookielib
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time, datetime

class Processor:
  def __init__(self):
    '''
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    
    client = MongoClient()
    self.db = client.author
    self.collection = self.db.AnalyticalChemistry
    ''' 
    
    # the module to generate the full url list
    pool = self.getURLlist()
    f = open("urlListAdvMat.txt", "w")
    for item in pool:
      f.write(item + "\n")

    '''
    
    # the module to read from txt
    with open("urlListAnaChem.txt") as f:
      pool = f.readlines()
    
    #pool = self.generateURL() 

    for url in pool:
      print url + "......."
      print datetime.datetime.now()
      content = urllib2.urlopen(url, timeout=60).read()
      self.parse(content)
    '''
    
  def generateURL(self):
    pool = []
    for vol in range (1,2):
      for issue in range(1, 6):
        url = "http://pubs.acs.org/toc/ancac3/" + str(vol) + "/" + str(issue)
        pool.append(url)
    for vol in range (2,9):
      for issue in range(1, 13):
        url = "http://pubs.acs.org/toc/ancac3/" + str(vol) + "/" + str(issue)
        pool.append(url)
    return pool 

  def getURLlist(self):
    output = []

    f = open('AdvMatFullList.html', 'r')
    content = f.read()
    soup = BeautifulSoup(content)
    out = soup.find_all(href=True)
    for item in out:
      url = item["href"]
      if ("http://onlinelibrary.wiley.com/doi/10.1002/adma" in url) and len(url) < 150:
        output.append(url)
    
    return output


  def getAffi(self, doi):
    url = "http://pubs.acs.org/doi/full/" +  doi
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    out = soup.findAll("div", {"class" : "affiliations"})
    print "the affi is " + out[0].text
    return out[0].text 

  def parse(self, content):
    soup = BeautifulSoup(content)
    titleAndAuthor = soup.findAll("div", {"class" : "titleAndAuthor"})
    #dates = soup.findAll("div", {"class" : "epubdate"})
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

      #affi    = self.getAffi(doi)

      comp["title"] = title
      comp["author"] = author 
      comp["date"] = date 
      comp["doi"] = doi 
      comp["type"] = typ 
      #comp["affiliations"] = affi 
      self.collection.insert(comp)
      print "save success " + comp["doi"]


def main():
  processor = Processor()

if __name__ == '__main__':
    main()





