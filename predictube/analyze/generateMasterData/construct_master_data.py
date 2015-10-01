import csv
import os
import datetime
from shutil import copyfile
def get_video_comments(dir_path, file_name):
	file_path = dir_path + file_name
	file_ = open(file_path,"r")
	file_data = file_.read()
	if file_data.startswith("Comments Forbidden in this video") or os.stat(file_path).st_size == 0:
		return 0
	tem = file_data
	val = file_data.split("***||***")
	if len(val) > 1:
		return 1
	return 0

def get_dic_comments(dir_path):
	file_names = os.listdir(dir_path)
	dic_comments = {}
	for file_name in file_names:
		comments = get_video_comments(dir_path, file_name)
		if comments:
			dic_comments[file_name] = 1
	return dic_comments

def get_dic_views(dir_path, dic_comments):
	file_names = os.listdir(dir_path)
	dic_views = {}
	line1 = []
	for file_name in file_names:
		if os.stat(dir_path + file_name).st_size != 0 and dic_comments.has_key(file_name):
			dic_views[file_name] = 1
			line1.append(file_name)
	return dic_views

def write_all_data(dir_path, dic_views):
	file_path = dir_path + "MasterData.csv"
	file_path2 = dir_path + "MasterData1.csv"
	ifile = open(file_path)
	ofile = open(file_path2, "w")
	reader = csv.reader(ifile)
	writer = csv.writer(ofile, delimiter=',')
	header = []
	data = []
	row_num = 0
	counter = 0
	for row in reader:
		if row_num == 0:
			header = row
			writer.writerow(header)
		elif dic_views.has_key(row[0]) and row[-1] != "NOT FOUND" and row[-2] != "NOT FOUND":
			counter+=1
			writer.writerow(row)
		row_num += 1
	ifile.close()
	ofile.close()
	print row_num
	print counter

def write_comments_views(dir_path, dir_path_comments, dir_path_views):
	file_path = dir_path + "MasterData.csv"
	ifile = open(file_path)
	reader = csv.reader(ifile)
	header = []
	row_num = 0
	for row in reader:
		if row_num != 0:
			copyfile(dir_path_comments+row[0],dir_path+"comments/" + row[0])
			copyfile(dir_path_views+row[0],dir_path+"views/" + row[0])
		row_num += 1
	ifile.close()

def get_video_comments(dir_path, file_name):
	file_path = dir_path + file_name
	file_ = open(file_path,"r")
	file_data = file_.read()
	val = file_data.split("***||***")
	comments = []
	for I in range(2,len(val),3):
		u=[]
		u.append(val[I])
		u.append(val[I+1].split("\n")[0])
		comments.append(u)
	file_.close()
	return (file_name, comments)

def get_all_comments(dir_path):
	file_names = os.listdir(dir_path)
	comments_data = []
	for file_name in file_names:
		comments = get_video_comments(dir_path, file_name)
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

def get_all_views(dir_path):
	file_names = os.listdir(dir_path)
	views_data = []
	for file_name in file_names:
		if os.stat(dir_path + file_name).st_size != 0 :
			views = get_video_views(dir_path, file_name)
			views_data.append(views)
	return views_data

def update_master_data(dir_path_comments, dir_path_views, dir_path):
	comments_data = get_all_comments(dir_path_comments)
	print "Done"
	views_data = get_all_views(dir_path_views)
	print "Done"
	dic_comments = {}
	dic_views = {} 
	for file_name,comments in comments_data:
		dic_comments[file_name] = len(comments)
	for file_name,publication_date,views in views_data:
		dic_views[file_name] = sum(views)

	file_path = dir_path + "MasterData.csv"
	file_path2 = dir_path + "MasterData1.csv"
	ifile = open(file_path)
	ofile = open(file_path2, "w")
	reader = csv.reader(ifile)
	writer = csv.writer(ofile, delimiter=',')
	header = []
	data = []
	row_num = 0
	counter = 0
	for row in reader:
		if row_num == 0:
			header = row
			writer.writerow(header+["comments count","views count"])
		else:
			counter+=1
			writer.writerow(row+[str(dic_comments[row[0]]),str(dic_views[row[0]])])
		row_num += 1
	ifile.close()
	ofile.close()

def run(dir_path):
	dir_path_comments = dir_path + "youtube_data/Comments Crawled/video_comments/"
	dir_path_views = dir_path + "youtube_data/Day wise views/views/"
	# dic_comments = get_dic_comments(dir_path_comments)
	# dic_views = get_dic_views(dir_path_views, dic_comments)
	# write_all_data(dir_path, dic_views)
	# write_comments_views(dir_path, dir_path_comments, dir_path_views)
	update_master_data(dir_path_comments, dir_path_views, dir_path)

def main():
	dir_path = "/Users/bp/Projects/SocialComputing/"
	run(dir_path)

if __name__ == '__main__':
	main()