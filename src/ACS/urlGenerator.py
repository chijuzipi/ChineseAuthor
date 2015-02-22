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
    f = open('archive/processed/test.txt', 'w')
    parentURL = "parentURL"
    for vol in range (2,10):
      for issue in range(1, 13):
        url = parentURL + str(vol) + "/" + str(issue)
        f.write(url + '\n')

  def confirm(self, url):
    critic1 = "http://pubs.acs.org/toc/inocaj" in url 
    critic3 = len(url) < 100
    if critic1 and critic3:
      return True
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

