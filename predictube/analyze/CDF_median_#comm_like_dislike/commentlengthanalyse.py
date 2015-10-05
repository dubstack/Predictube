import csv
import os
import datetime
import sys
from getCategory import getCategory
import matplotlib.pyplot as plt

working_directory='/home/bhushan/Documents/Soc_Comp_Project/SocialComputing_Master/SocialComputing_Master/'

def getCDF(numbers):
	if len(numbers)==0:
		return []
	out=[0 for i in range(max(numbers)+5)]
	for j in numbers:
		for k in range(j,len(out)):
			out[k]=out[k]+1
	mx=max(out)
	return [i/float(mx) for i in out]

def plotCombinedCDF(Xs,labels,tit):
	try:
		Xs.remove([])
	except:
		pass
	plt.figure()
	plt.title('CDF of median of comment length,#comments,likes,dislikes for category: '+tit)
	plt.ylabel('CDF')
	for X in range(len(Xs)):
		plt.plot([float(i)/len(Xs[X]) for i in range(len(Xs[X]))],Xs[X],label=labels[X])
	plt.legend()
	plt.savefig('CDF of median of comment length,#comments,likes,dislikes for category: '+tit+'.png')

def get_cat_video_dict(data):
	video_cat={}
	for row in data:
		video_cat[row[0]]=row[-3]
	return video_cat

def get_all_categories(data):
	list1 = []
	for row in data:
		list1.append(row[-3])
	list1 = set(list1)
	return list(list1)

def get_all_data(file_path):
	ifile = open(file_path)
	reader = csv.reader(ifile)
	header = []
	data = []
	row_num = 0
	for row in reader:
		if row_num == 0:
			header = row
		else:
			data.append(row)
		row_num += 1
	return header, data

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
		print file_name
		comments = get_video_comments(dir_path, file_name)
		comments_data.append(comments)
	return comments_data

def lengthanalysis(dir_path_comments,video_cat,categories):
	comments_data = get_all_comments(dir_path_comments)
	print "Done"
	dic={}
	for category in categories:
		MAX=[]
		MEDIAN=[]
		AVG=[]
		NO_OF_COMM=[]
		for file_name,comments in comments_data:
			if video_cat[file_name]==category:
				maxlength=0
				summ=0.0
				length=[]
				for comment in comments:
					text=comment[0].split()
					maxlength=max(len(text),maxlength)
					length.append(len(text))
					summ+=float(len(text))
				avg=summ/len(comments)
				length.sort()
				median=length[len(length)/2]
				MAX.append(maxlength)
				AVG.append(avg)
				MEDIAN.append(median)
				NO_OF_COMM.append(len(comments))
		dic[category]=[getCDF(MEDIAN),getCDF(NO_OF_COMM)]
	return dic
		#makecdfplot(MAX,"MAX",category)
		#makecdfplot(MEDIAN,"MEDIAN",category)
		#makecdfplot(AVG,"AVG",category)
		#makenormalisedcdf(MAX,MEDIAN,AVG,category)

def run():
	dir_path_category= working_directory + "MasterData.csv"
	header, data = get_all_data(dir_path_category)
	categories = get_all_categories(data)
	video_cat = get_cat_video_dict(data)
	dir_path_comments = working_directory + "comments/"
	lst=lengthanalysis(dir_path_comments,video_cat,categories)
	return lst

def main():
	dic=run()
	f=open(working_directory+'MasterData.csv','r')
	sdf=f.read().split('\n')
	ids=sdf[1:-1]
	f.close()
	categories=[i.split(',')[6] for i in ids]
	ctg=list(set(categories))
	for cat in ctg:
		likes=[int(ids[i].split(',')[2]) for i in range(len(ids)) if ids[i].split(',')[6]==cat]
		dislikes=[int(ids[i].split(',')[3]) for i in range(len(ids)) if ids[i].split(',')[6]==cat]
		likeCDF=getCDF(likes)
		dislikeCDF=getCDF(dislikes)
		dic[cat].append(likeCDF)
		dic[cat].append(dislikeCDF)
		labels=['median of comment length','No. of comments','like','dislike']
		plotCombinedCDF(dic[cat],labels,cat)

if __name__ == '__main__':
	main()
