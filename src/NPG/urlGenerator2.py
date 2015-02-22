from bs4 import BeautifulSoup

class URLGenerator:
  def __init__(self):

    # when the urls from file
    #self.generate()

    # when the urls can be direct synthesized
    self.synthesis()

  def synthesis(self):
    f = open('archive/processed/NatureCellBio.txt', 'w')
    parentURL = "http://www.nature.com/ncb/journal/"
    for vol in range (1,2):
      for issue in range(1, 9):
        url = parentURL + "v" + str(vol) + "/" + "n" + str(issue) + "/index.html"
        f.write(url + " " + str((vol + 1998))+'\n')
    for vol in range (2,17):
      for issue in range(1, 13):
        url = parentURL + "v" + str(vol) + "/" + "n" + str(issue) + "/index.html"
        f.write(url + " " + str((vol + 1998))+'\n')
    for vol in range (17,18):
      for issue in range(1, 3):
        url = parentURL + "v" + str(vol) + "/" + "n" + str(issue) + "/index.html"
        f.write(url + " " + str((vol + 1998))+'\n')

  def confirm(self, url):
    critic1 = "http://pubs.acs.org/toc/joceah" in url 
    critic3 = len(url) < 100
    if critic1 and critic3:
      return True
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

