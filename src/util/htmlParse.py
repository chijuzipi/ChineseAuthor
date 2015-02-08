from bs4 import BeautifulSoup

class HtmlParser:
  def __init__(self):
    f1 = open('issuelist/pinyin.html', 'r')
    f2 = open('issuelist/handian.txt', 'w')
    content = f1.read()
    soup = BeautifulSoup(content)
    out = soup.findAll("dt")
    for item in out:
      print item.text
      f2.write(item.text.encode('utf-8').strip() + "\n")

def main():
  parse = HtmlParser()

if __name__ == '__main__':
    main()

