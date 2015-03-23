f1 = open("given_name.txt", "r")
f2 = open("../../firstname_handian.txt", "r")
f3 = open("given_interaction.txt", "w")
lines1 = f1.readlines()
lines2 = f2.readlines()
amer = set()
for line1 in lines1:
  divid = line1.split()
  amer.add(divid[1])
  amer.add(divid[3])

for line2 in lines2:
  name = line2.rstrip()
  if name not in amer:
    f3.write(name+"\n")
  
