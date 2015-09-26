import matplotlib.pyplot as plt
import math
import numpy
from getCategory import getCategory
import os

def plot(X,Y,cat):
	print len(X)
	if len(X)==0:
		return
	plt.plot(X, Y, 'ro')
	plt.axis([min(X), max(X), min(Y), max(Y)])
	plt.ylabel('log(comments)')
	plt.xlabel('%-of likes')
	plt.title(cat)
	plt.show()

def comments_vs_likedislike(working_directory):
	dir='categorybased/'
	dirs=os.listdir(dir)
	dirs=[i.split('.')[0] for i in dirs]
	detail=open(working_directory+'MyCollection/channel_video_details.txt','r')
	details=detail.read().split('\n')[:-1]
	detail.close()
	details=sorted(details,key=lambda x:-int(x.split('\t')[-4]))
	catlist=[getCategory(details[i].split('\t')[0]) for i in range(len(details))]
	for cat in dirs:
		likes=[int(details[i].split('\t')[-3]) for i in range(len(details)) if catlist[i]==cat]
		dislikes=[int(details[i].split('\t')[-2]) for i in range(len(details)) if catlist[i]==cat]
		comments=[math.log(int(details[i].split('\t')[-1])+1) for i in range(len(details)) if catlist[i]==cat]
		normalised_ratio=[(float(likes[i]+1)*100.0/(float(likes[i]+1)+float(dislikes[i]+1))) for i in range(len(likes))]
		plot(normalised_ratio,comments,cat)

def main():
	working_directory='/home/bhushan/Documents/Soc_Comp_Project/youtube_data/'
	comments_vs_likedislike(working_directory)

if __name__=="__main__":
	main()
