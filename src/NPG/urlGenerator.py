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

    #find every <a href ... tag
    out = soup.find_all('a', href=True)
    for item in out:
      url = item['href'] 
      if self.confirm(url):
        date = item.find('dd', {'class' : 'published'}).text
        year = date.split()[2]

        f2.write(url + " " + year + " " + date + '\n')

  def getYear(self, itemid):
    return itemid.split('_')[1]

  def confirm(self, url):
    critic1 = "http://www.nature.com/nature/journal/" in url 
    critic2 = "supp" not in url
    critic3 = len(url) < 80
    if critic1 and critic2 and critic3:
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

