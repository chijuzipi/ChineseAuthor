f2 = open("NatureCommu2.txt", "w")

with open("NatureCommu.txt") as f:
  pool = f.readlines()

for line in pool:
  parts = line.split()
  url   = parts[0]
  year  = parts[1]
  f2.write(url + "/index.html/" + " " + year + '\n')
