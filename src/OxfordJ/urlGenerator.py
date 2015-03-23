import urllib2, cookielib
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time, datetime

class URLGenerator:
  def __init__(self):

    # when the urls from file
    self.generate()

    # when the urls can be direct synthesized
    #self.synthesis()

  def generate(self):
    f1 = open('archive/NAresearch.html', 'r')
    f2 = open('archive/processed/InorganicChem.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)

    #find every <a href ... tag
    out = soup.find_all(href=True)
    for item in out:
      url = item["href"]
      if self.confirm(url):
        f2.write(url + '\n')
  
  def synthesis(self):
    f = open('archive/processed/NAResearch.txt', 'w')
    parentURL = "http://nar.oxfordjournals.org/content/by/year/"
    for year in range (1974, 2016):
      url = parentURL + str(year)
      f.write(url + " " + str(year) +'\n')

  def confirm(self, url):
    critic1 = "http://pubs.acs.org/toc/inocaj" in url 
    critic3 = len(url) < 100
    if critic1 and critic3:
      return True
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

