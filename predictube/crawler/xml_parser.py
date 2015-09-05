from xml.dom import minidom
import os
import csv
import json

directory = '/home/aayush/Desktop/assign/socialComputing/data'



def export_to_file(video_stats):
	ofile = open('superwoman_statistics.csv','w')
	writer = csv.writer(ofile)
	writer.writerow(['id','day','watch_time_cumulative','watch_time_daily','shares_cumulative','shares_daily','subscribers_cumulative','subscribers_daily','views_cumulative','views_daily'])
	for key,value in video_stats.items():
		row = []
		if value.has_key('day'):
			row = row+[key]+[value['day']['data']]
		else:
			row = row+[[]]+[[]]
		if value.has_key('watch-time'):
			row = row+[value['watch-time']['cumulative']['data']]+[value['watch-time']['daily']['data']]
		else:
			row = row+[[]]+[[]]
		if value.has_key('shares'):
			row = row+[value['shares']['cumulative']['data']]+[value['shares']['daily']['data']]
		else:
			row = row+[[]]+[[]]
		if value.has_key('subscribers'):
			row = row+[value['subscribers']['cumulative']['data']]+[value['subscribers']['daily']['data']]
		else:
			row = row+[[]]+[[]]
		if value.has_key('views'):
			row = row+[value['views']['cumulative']['data']]+[value['views']['daily']['data']]
		else:
			row = row+[[]]+[[]]
		# print row	
		writer.writerow(row)

	ofile.close()




def get_processed_video(dataFileName):
	xmldoc = minidom.parse(dataFileName)
	rawdocuments = xmldoc.getElementsByTagName('graph_data')
	data = {}
	for document in rawdocuments:
		data = json.loads(document.firstChild.nodeValue)		
	return data



dir_level_1 = os.listdir(directory)

video_stats = {}

for directory_1 in dir_level_1:
	dir_level_2 = os.listdir(directory+'/'+directory_1)
	for directory_2 in dir_level_2:
		dir_level_3 = os.listdir(directory+'/'+directory_1+'/'+directory_2)
		for directory_3 in dir_level_3:
			dir_level_4 = os.listdir(directory+'/'+directory_1+'/'+directory_2+'/'+directory_3)
			for file in dir_level_4:
				video_stats[file] = get_processed_video(directory+'/'+directory_1+'/'+directory_2+'/'+directory_3+'/'+file)
			
export_to_file(video_stats)









