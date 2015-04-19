from stemming.porter2 import stem
import urllib2, cookielib
url = "http://stackoverflow.com/questions/735975/static-methods-in-python"
content = urllib2.urlopen(url, timeout=120).read()
print len(content)

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
