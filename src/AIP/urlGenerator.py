from bs4 import BeautifulSoup
import re

class URLGenerator:
  def __init__(self):

    # when the urls from file
    #self.generate()

    # when the urls can be direct synthesized
    self.synthesis2()

  def generate(self):
    f1 = open('archive/APLIssues.html', 'r')
    f2 = open('archive/processed/APL.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)

    #find every <a href ... tag
    #issueBar = soup.findAll("div", {"class":"issueBar"})
    flat = soup.find('ul', {"class":"flat"})
    lists = flat.findAll('li')
    print len(lists)
    return
    urls = issueBar.findAll("li", {"class":"issue"})
    print len(urls)
    return
    for urlEle in urls:
      url = urlEle['href'] 
      if self.confirm(url):
        print url
        #f2.write(url + " " + self.getYear(item['id']) + '\n')

  def getYear(self, itemid):
    return itemid.split('_')[1]

  def confirm(self, url):
    critic1 = "/content/aip/journal/apl/" in url
    if critic1:
      return True

  def synthesis(self):
    f = open('archive/processed/test.txt', 'w')
    parentURL = "http://scitation.aip.org/content/aip/journal/apl/"
    year = 1961
    for vol in range (1,107):
      for issue in range(1, 27):
        thisyear = str(year+vol)
        url = parentURL + str(vol) + "/" + str(issue)
        f.write(url + " " + thisyear + '\n')

  def synthesis2(self):
    f = open('archive/processed/APL.txt', 'w')
    parentURL = "http://scitation.aip.org/content/aip/journal/apl/"
    for vol in range (1,107):
      for issue in range(1, 27):
        url = parentURL + str(vol) + "/" + str(issue) + "?pageSize=10000&page=1"
        f.write(url + '\n')
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

