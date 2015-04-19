from pymongo import MongoClient

client = MongoClient()
db_chem = client.ACS
db_phys = client.APS
db_bio  = client.Cell

collection_chem = db_chem['JACS_coll']
collection_phys = db_phys['prl_coll']
collection_bio  = db_bio['Cell_coll']

cursor = collection_chem.find({"year":{'$gte':'1990', '$lt':'2010'}})
documents = list(cursor)
print len(documents)

