import urllib2
from TorCtl import TorCtl
import time

class URLlib2:
  def __init__(self):
    proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
    opener = urllib2.build_opener(proxy_support) 
    urllib2.install_opener(opener)
    self.conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="chijuzipi")

  def newId(self):
    self.conn.send_signal("NEWNYM")
    self.conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="chijuzipi")

  def readURL(self, url):
    req = urllib2.Request(url)
    try:
      resp = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
      print e.code
      #if e.code == 404:
      print "renew IP address ###################"
      self.newId()
      time.sleep(5)
      return self.readURL(url)

    except urllib2.URLError as e:
      print "connection refused"
      return self.readURL(url)

    else:
        # 200
        body = resp.read()
        return body
