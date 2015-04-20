from stem import Signal
from stem.control import Controller
import urllib2
from TorCtl import TorCtl

def changeId():
  with Controller.from_port(port = 9051) as controller:
    controller.authenticate("chijuzipi")
    controller.signal(Signal.NEWNYM)

def newId():
  conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="chijuzipi")
  conn.send_signal("NEWNYM")

for i in range(0, 10):
  print "case "+str(i+1)
  changeId()

  proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
  opener = urllib2.build_opener(proxy_support) 
  urllib2.install_opener(opener)
  url = "http://www.ifconfig.me/ip"
  url2 = "http://stackoverflow.com/questions/9887505/changing-tor-identity-inside-python-script"
  print len(urllib2.urlopen(url2).read())
  print urllib2.urlopen(url).read()
