from bs4 import BeautifulSoup

class ACSParser:
  def __init__(self, content):
    self.abstract = ''
    self.affi     = ''
    self.parse(content)

  def parse(self, content):
    soup = BeautifulSoup(content) 
    abstractEle = soup.find('div', {'id':'abstractBox'})
    if abstractEle is not None:
      self.abstract = abstractEle.find('p').text

    affiEle     = soup.find('div', {'class':'affiliations'})
    if affiEle is not None:
      affiList = affiEle.findAll('div')
      for item in affiList:
        if "$$" in item.text:
          print "*********** Found @ in negative text *******************"
        self.affi += item.text + "$$"


    if self.abstract == '':
      print "ABS is NONE"
    if self.affi == '':
      print "AFF is NONE"

      
  def getAffi(self):
    return self.affi

  def getAbs(self):
    return self.abstract
  
  @staticmethod
  def getUrl(coll, doi):
    if coll == "JACS_coll":
      return "http://pubs.acs.org/doi/abs/" + doi
    else:
      return""
    
     

