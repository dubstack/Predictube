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
	return out

def plotCombinedCDF(Xs,labels,tit):
	try:
		Xs.remove([])
	except:
		pass
	plt.title(tit)
	for X in range(len(Xs)):
		plt.plot([float(i)/len(Xs[X]) for i in range(len(Xs[X]))],Xs[X],label=labels[X])
	plt.legend()
	plt.show()

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
		dislikeCDF=getCDF(dislikes)
		labels=['like','dislike']
		plotCombinedCDF([likeCDF,dislikeCDF],labels,cat)

if __name__=='__main__':
	main()