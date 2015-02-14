from bs4 import BeautifulSoup
import re

class URLGenerator:
  def __init__(self):

    # when the urls from file
    self.generate()

    # when the urls can be direct synthesized
    #self.synthesis()

  def generate(self):
    f1 = open('archive/CellIssues.html', 'r')
    f2 = open('archive/processed/Cell.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)

    #find every <a href ... tag
    out = soup.find_all('a', href=True)
    for item in out:
      url = item['href'] 
      if self.confirm(url):
        info = item.text
        issue, year = self.getInfo(info)
        f2.write(url + " " + year + " " + issue + '\n')

  def getInfo(self, info):
    parts = info.split(',') 
    year  = parts[len(parts)-2]
    year  = year.split()
    year  = year[len(year)-1]
    issue = parts[0].split()
    issue = issue[len(issue)-1]
    return issue, year


  def confirm(self, url):
    critic1 = "http://www.cell.com/cell/issue?" in url 
    #critic2 = "supp" not in url
    #critic3 = len(url) < 80
    if critic1:
      return True

'''
  def synthesis(self):
    f = open('archive/processed/test.txt', 'w')
    parentURL = "parentURL"
    for vol in range (1,9):
      for issue in range(1, 13):
        url = parentURL + str(vol) + "/" + str(issue)
        f.write(url + '\n')
'''
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

