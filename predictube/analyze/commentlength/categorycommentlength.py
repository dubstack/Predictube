import os
import csv


#Take only those video ids from total data which we want to analyze.
#In this ids is a list of [video id,viewcount]
def EligibleIDs():
	ids = {}
	Dirs = os.listdir('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/categorybased/')
	for file in Dirs:
		if file!='categorymapping.txt' and file!='distributecategory.py':
			ifile = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/categorybased/'+file)
			lines = ifile.readlines()
			id = []
			for line in lines:
				component = line.split()
				id.append([component[0],component[1].strip()])
			ifile.close()
			ids[file.split('.')[0]] = id
			ifile.close()
	return ids


commentDir = '/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/Comments Crawled/video_comments/'

ids = EligibleIDs()
for key,value in ids.items():
	ofile = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/commentlength/'+key+'.csv','w')
	writer = csv.writer(ofile)
	writer.writerow(['VideoId','View Count','Average Comment Length','Total Comments'])
	for id in value:
		try:
			commentFile = open(commentDir+id[0])
		except:
			continue
		totalCommentLength = 0
		totalComments = 0
		i=0
		data = commentFile.read()
		components = data.split('***||***')
		for i in range(2,len(components),3):
			comment = components[i].decode('utf-8').encode('ascii','ignore')
			totalCommentLength = totalCommentLength + len(comment.split(' '))
			totalComments = totalComments + 1
		if totalComments==0:
			continue
		row = [id[0],id[1],str(float(totalCommentLength)/totalComments),totalComments]
		print row
		writer.writerow(row)
	ofile.close()
