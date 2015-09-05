import sys
import csv
import MySQLdb as mdb
import sqlite3
import time
sys.path.append('/home/aayush/Desktop/assign/socialComputing/YTCrawl-master')
from crawler import Crawler


def getId():
	con = sqlite3.connect('youtube-data-sqlite/youtube.sqlite')
	cur = con.cursor()
	sql = "SELECT id FROM youtube_statistics"
	ids = cur.execute(sql)
	return ids





ids = getId()

id_file = open('sqlite_id.txt','w')
for id in ids:
	id_file.write(id[0]+'\n')
id_file.close()





c = Crawler()
c._crawl_delay_time = 1.2
c._cookie_update_delay_time = 1
c.batch_crawl('sqlite_id.txt','/home/aayush/Desktop/assign/socialComputing/sqlite_data')

# ofile = open("youtube_data.csv",'w')
# errorFile = open("errorIds.csv",'w')
# writer = csv.writer(ofile)
# error_writer = csv.writer(errorFile)
# writer.writerow(['id','numShare','numSubscriber','watchTime','uploadDate','dailyViewCount'])

# c = Crawler()
# c._crawl_delay_time = 1 
# c._cookie_update_delay_time = 1

# for id in ids:
# 	i=0
# 	while 1:
# 		try:
# 			i=i+1
# 			data = c.single_crawl(id)
# 			print data
# 			writer.writerow([id,data['numShare'],data['numSubscriber'],data['watchTime'],data['uploadDate'],data['dailyViewcount']])
# 			break
# 		except:
# 			if i>=4:
# 				error_writer.writerow([id[0]])
# 				break
# 			continue


# errorFile.close()
# ofile.close()


