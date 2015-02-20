import urllib2, cookielib
from bs4 import BeautifulSoup
import time
import re

class URLGenerator:
  def __init__(self):
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    # when the urls from file
    self.generate()

    # when the urls can be direct synthesized
    #self.synthesis()

  def generate(self):
    f1 = open('archive/processed/PNASYear.txt', 'r')
    f2 = open('archive/processed/PNAS.txt', 'w')
    pool = f1.readlines()
    for url in pool:
      time.sleep(3)
      year = url.split('/')
      year = year[len(year)-1]
      print "processing " , url
      content = urllib2.urlopen(url, timeout=60).read()
      soup = BeautifulSoup(content)

      #find every <a href ... tag
      blocks = soup.findAll("td", {"class" : "proxy-archive-by-year-month"})
      for block in blocks:
        items = block.findAll(href=True)
        for item in items: 
          url = item["href"]
          url = "http://www.pnas.org" + url + " " + year
          #print url
          f2.write(url)
  
  def synthesis(self):
    f = open('archive/processed/PNASYear.txt', 'w')
    parentURL = "http://www.pnas.org/content/by/year/"
    for year in range (1915, 2016):
      url = parentURL + str(year)
      f.write(url + '\n')

  def confirm(self, url):
    critic1 = ("/content/") in url 
    critic3 = len(url) < 50
    if critic1 and critic3:
      return True
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

