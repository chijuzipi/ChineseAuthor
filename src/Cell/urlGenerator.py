from bs4 import BeautifulSoup
import re

class URLGenerator:
  def __init__(self):

    # when the urls from file
    #self.generate()

    # when the urls can be direct synthesized
    self.synthesis()

  def generate(self):
    f1 = open('archive/MolecularCellIssues.html', 'r')
    f2 = open('archive/processed/MolecularCell.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)

    #find every <a href ... tag
    out = soup.find_all('a', href=True)
    for item in out:
      url = item['href'] 
      if self.confirm(url):
        info   = item.text.rstrip()
        info   = re.compile(r'[\n\r\t]').sub(' ', info)
        divid = info.split(",")
        if len(divid) is 2:
          year =  divid[0].split()[1]
        elif len(divid) is 3:
          year =  divid[1].split()[0]
        f2.write(url + " " + year+ '\n')

  def synthesis(self):
    f = open('archive/processed/plosone.txt', 'w')
    parentURL1 = "http://www.plosone.org/browse/?startPage="
    parentURL2 = "&filterAuthors=&filterSubjectsDisjunction=&filterArticleTypes=&pageSize=13&filterKeyword=&filterJournals=PLoSONE&query=&ELocationId=&id=&resultView=list&sortValue=&unformattedQuery=*%3A*&sortKey=&filterSubjects=&volume=&"
    for page in range (0,9443):
      url = parentURL1 + str(page) + parentURL2 
      f.write(url+'\n')

  def getInfo(self, info):
    parts = info.split(',') 
    year  = parts[len(parts)-2]
    year  = year.split()
    year  = year[len(year)-1]
    issue = parts[0].split()
    issue = issue[len(issue)-1]
    return issue, year


  def confirm(self, url):
    critic1 = "http://www.cell.com/molecular-cell/issue?" in url 
    #critic2 = "supp" not in url
    #critic3 = len(url) < 80
    if critic1:
      return True
    
def main():
  generator = URLGenerator()

if __name__ == '__main__':
    main()

