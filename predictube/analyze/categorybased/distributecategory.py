import csv
import MySQLdb as mdb
import sqlite3

con = sqlite3.connect('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/SQLite3 Databases/youtube.sqlite')
cur = con.cursor()

idfile = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/obtainedFor91000/views.txt')
lines = idfile.readlines()
ids = []
for line in lines:
	ids.append(line.split()[0])
idfile.close()

baseDir = '/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/categorybased/'

categoryMapFile = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/categorybased/categorymapping.txt')
lines = categoryMapFile.readlines()
categoryIdMap = {}
categoryFile = {}
for line in lines:
	component = line.split()
	category = component[1].strip()
	if category not in categoryIdMap.values():
		file = category.replace(' ','').replace('/','')+'.txt'
		categoryFile[category] = open(baseDir+file,'w')
	categoryIdMap[component[0]] = category

noCategoryFound = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/categorybased/nocategoryfound.txt','w')
noIdFound = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/categorybased/idnotfountindb.txt','w')

for id in ids:
	query = "SELECT categoryid FROM youtube_snippet WHERE id='%s'"%(id)
	cur.execute(query)
	res = cur.fetchone()
	if res is None:
		noIdFound.write(id+'\n')
	elif res[0] not in categoryIdMap.keys():
		noCategoryFound.write(id+' '+res[0]+'\n')
	else:
		categoryFile[categoryIdMap[res[0]]].write(id+'\n')




con.close()
noCategoryFound.close()
for value in categoryFile.values():
	value.close()




