'''
*********** This class to construct first name from give set of characters
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''

class FirstnameConstrutor:
  def __init__(self):

    kanjiSet = set()
    f = open('../lib/kanji_pinyin_handian.txt', 'r')
    kanji = f.readlines()
    for item in kanji:
      kanjiSet.add(item.rstrip('\n'))

    self.construct(kanjiSet)

  def construct(self, kanjiSet):
    f2 = open("../lib/firstname.txt", "w")

    # using set to remove duplicates
    result = set()
    for item1 in kanjiSet:
      for item2 in kanjiSet:
        combine1 = item1+item2
        combine1 = combine1.title()
        combine2 = item1.title() + "-" + item2.title()
        result.add(combine1)
        result.add(combine2)
    for item in result:
      f2.write(item + "\n")


def main():
  firstnameConstrutor = FirstnameConstrutor()

if __name__ == '__main__':
  main()
