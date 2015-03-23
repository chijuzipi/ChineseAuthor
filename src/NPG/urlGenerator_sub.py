from bs4 import BeautifulSoup

class URLGenerator:
  def __init__(self):

    # when the urls from file
    #self.generate()

    # when the urls can be direct synthesized
    self.synthesis()

  def generate(self):
    f1 = open('archive/InorganicChemIssues.html', 'r')
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
    f = open('archive/processed/NatureChemistry.txt', 'w')
    parentURL = "http://www.nature.com/nchem/journal/"
    for vol in range (1, 2):
      for issue in range(1, 10):
        url = parentURL + "v" + str(vol) + "/" + "n" + str(issue) + "/index.html"
        f.write(url + " " + str((vol + 2008))+'\n')
    for vol in range (2, 7):
      for issue in range(1, 13):
        url = parentURL + "v" + str(vol) + "/" + "n" + str(issue) + "/index.html"
        f.write(url + " " + str((vol + 2008))+'\n')
    for vol in range (7,8):
      for issue in range(1, 4):
        url = parentURL + "v" + str(vol) + "/" + "n" + str(issue) + "/index.html"
        f.write(url + " " + str((vol + 2008))+'\n')

  def confirm(self, url):
    critic1 = "http://pubs.acs.org/toc/joceah" in url 
    critic3 = len(url) < 100
    if critic1 and critic3:
      return True
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

