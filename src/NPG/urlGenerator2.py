from bs4 import BeautifulSoup

class URLGenerator:
  def __init__(self):

    # when the urls from file
    self.generate()

    # when the urls can be direct synthesized
    #self.synthesis()

  def generate(self):
    f1 = open('archive/NatureGene/NatureGeneIssueList.html', 'r')
    f2 = open('archive/processed/NatureGene.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)

    #find every <a href ... tag
    out = soup.find_all(href=True)
    for item in out:
      url = item["href"]
      if self.confirm(url):
        f2.write(url + '\n')
  
  def synthesis(self):
    f = open('archive/processed/AccountChem.txt', 'w')
    parentURL = "http://pubs.acs.org/toc/achre4/"
    for vol in range (1,48):
      for issue in range(1, 13):
        url = parentURL + str(vol) + "/" + str(issue)
        year = str(vol + 1967)
        f.write(url + " " + year +'\n')
    for vol in range (48,49):
      for issue in range(1, 3):
        url = parentURL + str(vol) + "/" + str(issue)
        year = str(vol + 1967)
        f.write(url + " " + year +'\n')

  def confirm(self, url):
    critic1 = "http://www.nature.com/ng/journal/" in url 
    if critic1:
      return True
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

