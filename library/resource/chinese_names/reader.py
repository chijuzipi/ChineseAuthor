f1 = open('kanji_pinyin_handian.txt', 'r')
f2 = open('surname_handian.txt', 'w')
content = f1.readlines()
for item in content:
  f2.write(item.title())
