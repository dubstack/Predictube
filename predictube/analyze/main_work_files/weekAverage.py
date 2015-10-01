import os
import datetime
import re
import time
counter = 0
import url_marker
#get comments for a single video
def get_video_comments(dir_path, file_name):
	file_path = dir_path + file_name
	file_ = open(file_path,"r")
	file_data = file_.read()
	if file_data.startswith("Comments Forbidden in this video") or os.stat(file_path).st_size == 0:
		return (file_name,[])
	tem = file_data
	val = file_data.split("***||***")
	# print val
	comments = []
	
	for I in range(2,len(val),3):
		u=[]
		u.append(val[I])
		u.append(val[I+1].split("\n")[0])
		comments.append(u)
	file_.close()
	return (file_name, comments)

# Returns comments in the following format list of (videoId,list of comments on that video) 
# comments are like : ["safjnas","comment goes here", "timestamp"]
def get_all_comments(dir_path):
	file_names = os.listdir(dir_path)
	comments_data = []
	for file_name in file_names:
		comments = get_video_comments(dir_path, file_name)
		if len(comments[1]) != 0:
			comments_data.append(comments)
	return comments_data

# get views for a single video
def get_video_views(dir_path, file_name):
	file_path = dir_path + file_name
	data = [line.rstrip('\n') for line in open(file_path)]
	publication_date = data[0].split()[-1]
	data = data[1:]
	views = []
	for day in data:
		if day.startswith("Published"):
			break
		val = day.split("\t")
		views.append(int(val[1]))
	return (file_name,publication_date,views)

# return views of videos having atleast one comment
def get_all_views_having_comments(dir_path, video_ids_with_comments):
	file_names = os.listdir(dir_path)
	# global counter
	views_data = []
	for file_name in file_names:
		if os.stat(dir_path + file_name).st_size != 0 and video_ids_with_comments.has_key(file_name):
			# counter+=1
			views = get_video_views(dir_path, file_name)
			views_data.append(views)
	# print counter
	return views_data

# Return views of all videos
def get_all_views(dir_path):
	file_names = os.listdir(dir_path)
	views_data = []
	for file_name in file_names:
		if os.stat(dir_path + file_name).st_size != 0 :
			views = get_video_views(dir_path, file_name)
			views_data.append(views)
	return views_data

# Utility Function to write list of video to file
def write_to_file_list_ids(ranked_list_ids):
	f=open('urls.txt','w')
	for x in ranked_list_ids:
		f.write(str(x[2])+' '+str(x[0])+' '+str(x[1])+'\n')
	f.close()

# Utility function to read list of videos from file
def read_from_file_list_ids():
	X=[]
	with open('ranked_video_ids.txt','r') as f:
		for line in f:
			line=line[:-1]
			x=line.split()
			u=[]
			u.append(int(x[0]))
			u.append(int(x[1]))
			u.append(int(x[2]))
			X.append(u)
	return X

#get dictionary of video ids having atleast one comment
def get_video_ids_with_comments(comments_data):
	dic = {}
	for video_id, comments in comments_data:
		dic[video_id] = 1
	return dic

#get dictionary of video ids having atleat one comment and one view
def get_relevant_video_ids(views_data):
	dic = {}
	for val in views_data:
		dic[val[0]] = 1
	return dic

# get comments data for all video in relevant video ids
def get_relvant_comments_data(comments_data, relevant_dic_ids):
	relevant_comments_data = []
	for video in comments_data:
		if relevant_dic_ids.has_key(video[0]):
			relevant_comments_data.append(video)
	return relevant_comments_data

#utility function to be used as an comparator function for the sorting
def getKey(item):
	return item[0]

# get Ranked ids of videos
def get_ranked_ids(relevant_views_data, relevant_comments_data):
	ranked_list_ids = []
	for i in range(len(relevant_comments_data)):
		ranked_list_ids.append((sum(relevant_views_data[i][2]), len(relevant_comments_data[i][1]), relevant_comments_data[i][0]))
	
	ranked_list_ids = sorted(ranked_list_ids, key = getKey, reverse = True)
	return ranked_list_ids

def write_daily_data(relevant_views_data, relevant_comments_data):
	dir_path = "/Users/bp/Projects/SocialComputing/video_views_comments/"
	for i in range(len(relevant_comments_data)):
		out=open(dir_path+relevant_comments_data[i][0]+'.txt','w')
		publication_date = datetime.datetime.strptime(relevant_views_data[i][1],'%Y-%m-%d')
		ccnt = [0 for k in range(len(relevant_views_data[i][2]))]
		for comm in relevant_comments_data[i][1]:
			tm = comm[1]
			dt2=datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.gmtime(int(tm)/1000.)),'%Y-%m-%d')
			# print dt2
			# print publication_date
			day=(dt2- publication_date).days
			if day>=0 and day <= (len(relevant_views_data[i][2])-1):
				ccnt[day]+=1
		for t in range(len(relevant_views_data[i][2])):
			out.write(str(relevant_views_data[i][2][t])+ ' ' +str(ccnt[t])+'\n')
		out.close()

def run1():
	# the directory location of the video comments
	dir_path_comments = "/Users/bp/Projects/SocialComputing/youtube_data/Comments Crawled/video_comments/"
	dir_path_views = "/Users/bp/Projects/SocialComputing/youtube_data/Day wise views/views/"
	comments_data = get_all_comments(dir_path_comments)
	video_ids_with_comments = get_video_ids_with_comments(comments_data)
	relevant_views_data = get_all_views_having_comments(dir_path_views, video_ids_with_comments)
	
	relevant_dic_ids = get_relevant_video_ids(relevant_views_data)
	relevant_comments_data = get_relvant_comments_data(comments_data, relevant_dic_ids)
	
	relevant_comments_data = sorted(relevant_comments_data, key = getKey)
	relevant_views_data = sorted(relevant_views_data, key = getKey)
	ranked_list_ids = get_ranked_ids(relevant_views_data, relevant_comments_data)
	print len(ranked_list_ids)
	write_to_file_list_ids(ranked_list_ids)

	write_daily_data(relevant_views_data, relevant_comments_data)
	# analyze(comments_data)

def run2():
	dir_path_comments = "/Users/bp/Projects/SocialComputing/youtube_data/Comments Crawled/video_comments/"
	comments_data = get_all_comments(dir_path_comments)
	video_ids_with_comments = get_video_ids_with_comments(comments_data)

	data = [line.rstrip('\n') for line in open("/Users/bp/Projects/SocialComputing/youtube_data/obtainedFor91000/views.txt")]
	counter= 0 
	for line in lines:
		va = line.split()
		if video_ids_with_comments.has_key(va[0]):
			counter+=1
	print counter

def main():
	run1()
	# run2()

#check number of Hyperlinks
def analyze(comments_data):
	dic = {}
	data = [line.rstrip('\n') for line in open("/Users/bp/Projects/SocialComputing/ranked_video_ids.txt")]
	for line in data:
		va = line.split()
		dic[va[0]] = va[1]

	relevant_comments_data = get_relvant_comments_data(comments_data, dic)
	p = re.compile(url_marker.WEB_URL_REGEX)
	res = []
	for video_id,comments in relevant_comments_data:
		cout = 0
		for comment in comments:
			li = p.findall(comment[0])
			if len(li) != 0:
				print li
				for l in li:
					if l != "":
						cout += 1
		res.append((dic[video_id],cout, video_id))
	res = sorted(res,reverse =True, key = getKey)
	# write_to_file_list_ids(res)


if __name__ == '__main__':
	main()
