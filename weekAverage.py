import os
import datetime
import time

def get_video_comments(dir_path, file_name):
	file_path = dir_path + file_name
	file_ = open(file_path,"r")
	file_data = file_.read()
	if file_data.startswith("Comments Forbidden in this video") or os.stat(file_path).st_size == 0:
		return []
	tem = file_data
	file_data = file_data.split(file_name+'***||***')[1:]
	comments = []
	for comment in file_data :
		values = comment.split("***||***")
		values = [val.strip() for val in values]
		comments.append(values)
	file_.close()
	return comments

# Returns comments in the following format list of (videoId,list of comments on that video) 
# comments are like : ["safjnas","comment goes here", "timestamp"]

def get_all_comments(dir_path):
	file_names = os.listdir(dir_path)
	comments_data = []
	for file_name in file_names:
		comments = get_video_comments(dir_path, file_name)
		comments_data.append((file_name,comments))
	return comments_data

def main():
	# the directory location of the video comments
	dir_path = "/Users/bp/Projects/SocialComputing/youtube_data/Comments Crawled/video_comments/"
	comments_data = get_all_comments(dir_path)

	# get_all_views()

if __name__ == '__main__':
	main()