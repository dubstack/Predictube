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
	plt.title('CDF of likes,dislikes for category: '+tit)
	plt.ylabel('CDF')
	for X in range(len(Xs)):
		plt.plot([float(i)/len(Xs[X]) for i in range(len(Xs[X]))],Xs[X],label=labels[X])
	plt.legend()
	plt.savefig('CDF of likes,dislikes for category: '+tit+'.png')

def plotIndividual(Y,label,tit):
	if len(Y)==0:
		return
	plt.figure()
	X=[i for i in range(len(Y))]
	plt.title('CDF of '+label+' for category: '+tit)
	plt.ylabel('CDF')
	plt.xlabel(label)
	plt.plot(X,Y)
	plt.savefig('CDF of '+label+' for category: '+tit+'.png')

def main():
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
		plotIndividual(likeCDF,'likes',cat)
		dislikeCDF=getCDF(dislikes)
		plotIndividual(dislikeCDF,'dislikes',cat)
		labels=['like','dislike']
		plotCombinedCDF([likeCDF,dislikeCDF],labels,cat)

if __name__=='__main__':
	main()