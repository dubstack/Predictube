import matplotlib.pyplot as plt
import math

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
	likes=[int(details[i].split('\t')[-3]) for i in range(len(details))]
	dislikes=[int(details[i].split('\t')[-2]) for i in range(len(details))]
	comments=[math.log(int(details[i].split('\t')[-1])+1) for i in range(len(details))]
	normalised_ratio=[math.log(float(likes[i]+1)/float(dislikes[i]+1)) for i in range(len(likes))]
	plot(normalised_ratio,comments)


	"""top1000=open(working_directory+'MyCollection/top_1000id.txt','r')
	top1000id=top1000.read().split('\n')[:-1]
	print top1000id[0]
	top1000.close()
	top10000=open(working_directory+'MyCollection/top_10000id.txt','r')
	top10000id=top10000.read().split('\n')[:-1]
	top10000.close()
	datadirectory=working_directory+'obtainedFor91000/Scatter/'
	like=open(datadirectory+'viewcount_likes.dat','r')
	dislike=open(datadirectory+'viewcount_dislikes.dat','r')
	comment=open(datadirectory+'viewcount_comment.dat','r')
	likes=like.read().split('\n')[:-1]
	print likes[0].split('\t')
	dislikes=dislike.read().split('\n')[:-1]
	comments=comment.read().split('\n')[:-1]
	like.close()
	dislike.close()
	comment.close()"""
	

def main():
	working_directory='/home/bhushan/Documents/Soc_Comp_Project/youtube_data/'
	comments_vs_likedislike(working_directory)

if __name__=="__main__":
	main()

