from bs4 import BeautifulSoup

class WileyParser:
  def __init__(self, content):
    self.abstract = ''
    self.affi     = ''
    self.key      = ''
    self.parse(content)

  def parse(self, content):
    soup = BeautifulSoup(content) 

    abstractEle = soup.find('div', {'id':'abstract'})
    if abstractEle is not None:
      self.abstract = abstractEle.find('p').text

    keywordEle  = soup.find('div', {'id':'keywordLists'})
    if keywordEle is not None:
      self.key = keywordEle.text

    affiList     = soup.findAll('li', {'class':'affiliation'})
    if len(affiList) != 0:
      for item in affiList:
        if "$$" in item.find('p').text:
          print "*********** Found @ in negative text *******************"
        self.affi += item.find('p').text + "$$" 


    if self.abstract == '':
      print "ABS is NONE"
    if self.affi == '':
      print "AFF is NONE"

      
  def getAffi(self):
    return self.affi

  def getAbs(self):
    return self.abstract

  def getKey(self):
    return self.key

def getUrl(coll, doi):
  if coll == "AdvFunMaterial_coll":
    return "http://onlinelibrary.wiley.com/doi/" + doi + "/abstract"
  else:
    return""
