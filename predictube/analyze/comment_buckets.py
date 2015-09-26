from datetime import datetime
import os
import matplotlib.pyplot as plt
import math
import numpy

def plot(X,Y):
	print len(X)
	plt.plot(X, Y, 'ro')
	plt.axis([min(X), max(X), min(Y), max(Y)])
	plt.ylabel('#comments')
	plt.xlabel('time of day')
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
	plot([i for i in range(24)],hourbuckets)
	#plot([i for i in range(7)],weekbuckets)
	print hourbuckets, weekbuckets

if __name__=="__main__":
	main()