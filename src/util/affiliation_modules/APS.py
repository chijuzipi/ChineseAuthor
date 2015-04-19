from bs4 import BeautifulSoup

class APSParser:
  def __init__(self, content):
    self.abstract = ''
    self.affi     = ''
    self.parse(content)

  def parse(self, content):
    soup = BeautifulSoup(content) 
    abstractEle = soup.find('section', {'data-magellan-destination':'abstract'})
    if abstractEle is not None:
      self.abstract = abstractEle.find('p').text

    affiEle     = soup.find('section', {'data-magellan-destination':'authors'})
    if affiEle is not None:
      affiInner = affiEle.find('ul', {'class':'no-bullet'})
      if affiInner is not None:
        affiList = affiInner.findAll('li')
        for item in affiList:
          if "$$" in item.text:
            print "*********** Found @ in negative text *******************"
          self.affi += item.text + "$$"


    if self.abstract == '':
      print "ABS is None"
    if self.affi == '':
      print "AFF is NONE"

      
  def getAffi(self):
    return self.affi

  def getAbs(self):
    return self.abstract

def getUrl(coll, doi):
  if coll == "prl_coll":
    return "http://journals.aps.org/prl/abstract/" + doi
  else:
    return ""
    
     

