import urllib2
from TorCtl import TorCtl

proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
opener = urllib2.build_opener(proxy_support) 
urllib2.install_opener(opener)

conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="chijuzipi")

def newId():
  conn.send_signal("NEWNYM")


def readURL(url):
  req = urllib2.Request(url)
  try:
    resp = urllib2.urlopen(req)
  except urllib2.HTTPError as e:
    return e.code
  except urllib2.URLError as e:
    return "connection refused"
  else:
      # 200
      body = resp.read()
      print body
      return 200
  
for i in range(0, 10):
  print "case "+str(i+1)
  newId()
  url1 = "http://www.ifconfig.me/ip"
  url2 = "http://journals.aps.org/prl/abstract/10.1103/PhysRevLett.114.143002"
  code = readURL(url1)
  while code != 200: 
    print "not getting 200, try again: " + str(code)
    code = readURL(url1)
  print len(urllib2.urlopen(url2).read())
