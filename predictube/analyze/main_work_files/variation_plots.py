from datetime import datetime
import os
import matplotlib.pyplot as plt
import math
import numpy
from weekAverage import get_all_comments

def plot(X,Y):
	diff = max(Y) - min(Y)
	plt.plot(X, Y, marker = 'o', color = "r")
	plt.axis([min(X), max(X), min(Y) - diff/5.0 , max(Y) + diff/5.0])
	plt.ylabel('#comments')
	if len(X)==24:
		plt.title("Hourly variation in commenting activity")
		plt.xlabel('hour of day')
	else:
		plt.title("Daily variation in commenting activity")
		plt.xlabel('Day of week')
	plt.show()

def bucket(comments_data):
	# weekdays returned as 0:Monday 1:Tuesday ... 6:Sunday
	# hours as usual
	hourbuckets=[0 for i in range(24)]
	weekbuckets=[0 for i in range(7)]
	for video_id,comments in comments_data:
		for comment in comments:
			dt = datetime.fromtimestamp(int(comment[1])/1000.0)
			hourbuckets[dt.hour]+=1
			weekbuckets[dt.weekday()]+=1

	return hourbuckets,weekbuckets

def main():
	dir_path_comments = "/Users/bp/Projects/SocialComputing/youtube_data/Comments Crawled/video_comments/"
	comments_data = get_all_comments(dir_path_comments)
	hourbuckets,weekbuckets = bucket(comments_data)
	plot([i+1 for i in range(24)],hourbuckets)
	plot([i+1 for i in range(7)],weekbuckets)

if __name__ == '__main__':
	main()

