import os
import csv


#Take only those video ids from total data which we want to analyze.
#In this ids is a list of [video id,viewcount]
def EligibleIDs():
	ifile = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/obtainedFor91000/views.txt')
	lines = ifile.readlines()
	ids = []
	for line in lines:
		ids.append(line.split())
	ifile.close()
	return ids


commentDir = '/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/Comments Crawled/video_comments/'
ofile = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/commentlength/commentlength.csv','w')
noCommentFile = open('/home/aayush/Desktop/assign/socialComputing/youtube_data(1)/commentlength/nocomments.txt','w')
writer = csv.writer(ofile)
writer.writerow(['VideoId','View Count','Average Comment Length'])
ids = EligibleIDs()
for id in ids:
	try:
		commentFile = open(commentDir+id[0])
	except:
		noCommentFile.write(id[0]+' No file present\n')
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
		noCommentFile.write(id[0]+' No comments in file\n')
		continue
	row = [id[0],id[1],str(float(totalCommentLength)/totalComments)]
	print row
	writer.writerow(row)
noCommentFile.close()
ofile.close()
