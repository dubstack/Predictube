from datetime import datetime

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
		tm=int(i.split('***||***')[-1])
		print tm
		dt=datetime.fromtimestamp(tm/1000)
		hourbuckets[dt.hour]+=1
		weekbuckets[dt.weekday()]+=1
	return hourbuckets,weekbuckets

def main():
	working_directory='/home/bhushan/Documents/Soc_Comp_Project/youtube_data/'
	video_id='ecXYTGox7HY'
	hourbuckets, weekbuckets = bucket(working_directory,video_id) 
	print hourbuckets, weekbuckets

if __name__=="__main__":
	main()