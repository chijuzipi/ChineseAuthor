from bs4 import BeautifulSoup
import re

class URLGenerator:
  def __init__(self):

    # when the urls from file
    self.generate()

    # when the urls can be direct synthesized
    #self.synthesis()

  def generate(self):
    f1 = open('archive/AdvMaterialIssues.html', 'r')
    f2 = open('archive/processed/AdvMaterial.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)

    #find every <a href ... tag
    out = soup.find_all('li', {'id': re.compile('year_*')})
    for item in out:
      urls = item.findAll(href=True)
      for urlEle in urls:
        url = urlEle['href'] 
        if self.confirm(url):
          f2.write(url + " " + self.getYear(item['id']) + '\n')

  def getYear(self, itemid):
    return itemid.split('_')[1]

  def confirm(self, url):
    critic1 = "http://onlinelibrary.wiley.com/doi/10.1002" in url 
    critic3 = len(url) < 150
    if critic1 and critic3:
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

