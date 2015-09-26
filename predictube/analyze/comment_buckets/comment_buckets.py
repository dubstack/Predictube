from datetime import datetime
import os
import matplotlib.pyplot as plt
import math
import numpy

def plot(X,Y):
	plt.plot(X, Y, 'ro')
	plt.axis([min(X)-1, max(X), min(Y)-100, max(Y)+100])
	plt.ylabel('#comments')
	if len(X)==24:
		plt.xlabel('hour of day')
	else:
		plt.xlabel('weekday')
	plt.show()

def bucket(working_directory,video_id):
	# weekdays returned as 0:Monday 1:Tuesday ... 6:Sunday
	# hours as usual
	hourbuckets=[0 for i in range(24)]
	weekbuckets=[0 for i in range(7)]
	try:
		f=open(working_directory+'Comments Crawled/video_comments/'+video_id,'r')
	except:
		print "no such file"
		return hourbuckets,weekbuckets
	comm=f.read().split(video_id+'***||***')[1:]
	for i in comm:
		try:
			tm=int(i.split('***||***')[-1])
			dt=datetime.fromtimestamp(tm/1000)
			hourbuckets[dt.hour]+=1
			weekbuckets[dt.weekday()]+=1
		except:
			pass
	return hourbuckets,weekbuckets

def main():
	working_directory='/home/bhushan/Documents/Soc_Comp_Project/youtube_data/'
	hourbuckets=[0 for i in range(24)]
	weekbuckets=[0 for i in range(7)]
	dirs=os.listdir(working_directory+'Comments Crawled/video_comments/')
	for fl in dirs:
		hb, wb = bucket(working_directory,fl)
		hourbuckets=[hourbuckets[i]+hb[i] for i in range(24)]
		weekbuckets=[weekbuckets[i]+wb[i] for i in range(7)]
	plot([i+1 for i in range(24)],hourbuckets)
	plot([i+1 for i in range(7)],weekbuckets)
	print hourbuckets, weekbuckets

# for our data: hourbuckets=[484280, 476082, 450082, 415858, 372862, 322483, 279622, 237281, 211177, 200547, 201263, 214988, 239696, 276273, 317489, 359266, 395048, 424540, 449011, 477380, 508320, 518507, 507467, 494051]
# for our data: weekbuckets=[1253323, 1244601, 1269488, 1216702, 1259317, 1285270, 1304872]

if __name__=="__main__":
	main()