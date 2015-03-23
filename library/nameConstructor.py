'''
*********** This class to construct first name from give set of characters
  (c) 2015 by Chad Zhou
  Northwestern University
**************************************************************************
'''

class FirstnameConstrutor:
  def __init__(self):

    f1 = open('resource/chinese_names/kanji_pinyin_handian_simple.txt', 'r')
    f2 = open('resource/american_names/given_name.txt', 'r')
    f3 = open('resource/american_names/last_name.txt', 'r')
    self.construct_given_name(f1, f2, f3)

  def construct_given_name(self, f, f2, f3):

    kanjiSet = set()
    amerSet  = set()
    kanji = f.readlines()
    amer_given = f2.readlines()
    amer_sur   = f3.readlines()
    
    # build kanjiSet
    for item in kanji:
      kanjiSet.add(item.rstrip('\n'))

    # build amerSet 
    for line in amer_given:
      divid = line.split()
      amerSet.add(divid[1])
      amerSet.add(divid[3])
    '''
    for line in amer_sur:
      divid = line.split()
      amerSet.add(divid[0].lower().title())
    '''
    f2 = open("given_name_simple_remove.txt", "w")

    # using set to remove duplicates
    result = set()
    for item1 in kanjiSet:
      for item2 in kanjiSet:
        combine1 = item1+item2
        combine1 = combine1.title()
        if combine1 not in amerSet:
          combine2 = item1.title() + "-" + item2.title()
          result.add(combine1)
          result.add(combine2)
        else:
          print "found bug: " + combine1
    for item in result:
      f2.write(item + "\n")



def main():
  firstnameConstrutor = FirstnameConstrutor()

if __name__ == '__main__':
  main()
