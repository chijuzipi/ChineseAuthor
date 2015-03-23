from bs4 import BeautifulSoup
import re

class URLGenerator:
  def __init__(self):

    # when the urls from file
    self.generate()

    # when the urls can be direct synthesized
    #self.synthesis()

  def generate(self):
    f1 = open('archive/NatureIssues.html', 'r')
    f2 = open('archive/processed/Nature.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)

    groups = soup.findAll('li', {'class' : 'expanded'})
    for group in groups:
      year = group.find('h2').text
      urls = group.findAll(href=True)
      for urlEle in urls:
        url = urlEle['href']
        if self.confirm(url):
          f2.write(url + " " + year + '\n')


  def getYear(self, itemid):
    return itemid.split('_')[1]

  def confirm(self, url):
    critic1 = "http://www.nature.com/nature/journal/" in url 
    critic2 = "supp" not in url
    critic3 = len(url) < 80
    if critic1 and critic2 and critic3:
      return True

  def synthesis(self):
    f = open('archive/processed/NatureCommu.txt', 'w')
    parentURL = "http://www.nature.com/ncomms/archive/date/"

    for year in range (2010, 2011):
      for mon in range(4, 13):
        yearstr  = str(year)
        monstr   = str(mon) if len(str(mon)) == 2 else '0'+str(mon)
        url = parentURL + yearstr + "/" + monstr
        f.write(url + '\n')

    for year in range (2011, 2015):
      for mon in range(1, 13):
        yearstr  = str(year)
        monstr   = str(mon) if len(str(mon)) == 2 else '0'+str(mon)
        url = parentURL + yearstr + "/" + monstr
        f.write(url + '\n')

    for year in range (2015, 2016):
      for mon in range(1, 3):
        yearstr  = str(year)
        monstr   = str(mon) if len(str(mon)) == 2 else '0'+str(mon)
        url = parentURL + yearstr + "/" + monstr
        f.write(url + '\n')
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

