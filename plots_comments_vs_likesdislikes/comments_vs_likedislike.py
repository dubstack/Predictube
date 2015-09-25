import matplotlib.pyplot as plt
import math
import numpy

#pearson=numpy.corrcoef(X, Y)[0, 1]

def pearson(details):
	class1=[i for i in details if int(i.split('\t')[-4])<=1000]
	class2=[i for i in details if int(i.split('\t')[-4])>1000 and int(i.split('\t')[-4])<=10000]
	class3=[i for i in details if int(i.split('\t')[-4])>10000 and int(i.split('\t')[-4])<=100000]
	class4=[i for i in details if int(i.split('\t')[-4])>1000000]
	pearson1=numpy.corrcoef([int(i.split('\t')[-4]) for i in class1],[int(i.split('\t')[-1]) for i in class1])[0,1]
	pearson2=numpy.corrcoef([int(i.split('\t')[-4]) for i in class2],[int(i.split('\t')[-1]) for i in class2])[0,1]
	pearson3=numpy.corrcoef([int(i.split('\t')[-4]) for i in class3],[int(i.split('\t')[-1]) for i in class3])[0,1]
	pearson4=numpy.corrcoef([int(i.split('\t')[-4]) for i in class4],[int(i.split('\t')[-1]) for i in class4])[0,1]
	print pearson1,pearson2,pearson3,pearson4

def plot(X,Y):
	print len(X)
	plt.plot(X, Y, 'ro')
	plt.axis([min(X), max(X), min(Y), max(Y)])
	plt.ylabel('log(comments)')
	plt.xlabel('log(ratio:likes/dislikes)')
	plt.show()

def comments_vs_likedislike(working_directory):
	detail=open(working_directory+'MyCollection/channel_video_details.txt','r')
	details=detail.read().split('\n')[:-1]
	detail.close()
	details=sorted(details,key=lambda x:-int(x.split('\t')[-4]))
	pearson(details)
	likes=[int(details[i].split('\t')[-3]) for i in range(10000)]
	dislikes=[int(details[i].split('\t')[-2]) for i in range(10000)]
	comments=[math.log(int(details[i].split('\t')[-1])+1) for i in range(10000)]
	normalised_ratio=[(float(likes[i]+1)*100.0/(float(likes[i]+1)+float(dislikes[i]+1))) for i in range(len(likes))]
	plot(normalised_ratio,comments)

def main():
	working_directory='/home/bhushan/Documents/Soc_Comp_Project/youtube_data/'
	comments_vs_likedislike(working_directory)

if __name__=="__main__":
	main()
