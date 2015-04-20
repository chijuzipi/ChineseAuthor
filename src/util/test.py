from stemming.porter2 import stem
import urllib2
url1 = "http://localhost:8080/"
url2 = "http://www.python.org/fish.html"
url3 = "http://stackoverflow.com/questions/1726402/in-python-how-do-i-use-urllib-to-see-if-a-website-is-404-or-200"
req = urllib2.Request(url2)
try:
  resp = urllib2.urlopen(req)
except urllib2.HTTPError as e:
  if e.code == 404:
    print "404"     
  else:
    print "code is not 404"
except urllib2.URLError as e:
  print "conection refused"
else:
    # 200
    body = resp.read()
    print len(body)


'''
documents = "highly"
divid = documents.split()
for word in divid:
  word = word.lower()
  word = stem(word) 
  print word


word = "x1u3"
if word[0] != 'p':
  print "False"
for char in word[1:]:
  print char
  if char > '9' or char < '0':
    print "False"

print "True"


oldList = ["1", "2", "3"]
newList = oldList[:len(oldList)-2]
print newList
'''
