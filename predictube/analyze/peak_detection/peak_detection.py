import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def getVideoIds():
	ifile = open('../generateMasterData/MasterData.csv')
	reader = csv.reader(ifile)
	videoIds = []
	next(reader)
	for row in reader:
		videoIds.append(row[0])
	return videoIds




def getDailyViewCount(videoId):
	dir = '../../data/Day wise views/views/'
	ifile = open(dir+videoId)
	lines = ifile.readlines()
	dailyViewCount = []
	firstLine=True
	for line in lines:
		if firstLine:
			firstLine = False
		else:
			comp = line.split()
			if comp[0]=='Published':
				break
			dailyViewCount.append(int(comp[1].strip()))
	return dailyViewCount



def getLocalPeaks(dailyViewCount):
	peaks = []
	k=1
	for i in range(len(dailyViewCount)):
		if i==0:
			x_left = dailyViewCount[i]
		else:
			x_left = max(dailyViewCount[max(0,i-k):i])
		if i==len(dailyViewCount)-1:
			x_right = dailyViewCount[i]
		else:
			x_right = max(dailyViewCount[i+1:min(i+k+1,len(dailyViewCount))])
		M = float(x_left + x_right)/2
		if dailyViewCount[i] > M:
			peaks.append((i+1,dailyViewCount[i]))
	return peaks

def getLocalValleys(dailyViewCount):
	valleys = []
	k=1
	for i in range(len(dailyViewCount)):
		if i==0:
			x_left = dailyViewCount[i]
		else:
			x_left = min(dailyViewCount[max(0,i-k):i])
		if i==len(dailyViewCount)-1:
			x_right = dailyViewCount[i]
		else:
			x_right = min(dailyViewCount[i+1:min(i+k+1,len(dailyViewCount))])
		M = float(x_left + x_right)/2
		if dailyViewCount[i] < M:
			valleys.append((i+1,dailyViewCount[i]))
	return valleys



def getSignificantPeaks(dailyViewCount):
	significantPeaks = []
	localPeaks = []
	S = []
	
	k=1
	for i in range(len(dailyViewCount)):
		if i==0:
			x_left = dailyViewCount[i]
		else:
			x_left = max(dailyViewCount[max(0,i-k):i])
		if i==len(dailyViewCount)-1:
			x_right = dailyViewCount[i]
		else:
			x_right = max(dailyViewCount[i+1:min(i+k+1,len(dailyViewCount))])
		if dailyViewCount[i] > (x_left + x_right)/2.0 : 
			localPeaks.append((i+1,dailyViewCount[i]))
			S.append(((dailyViewCount[i]-x_left) + (dailyViewCount[i]-x_right))/2.0)

	mean = np.mean(S)
	std = np.std(S)
	maxPeak = max([x[1] for x in localPeaks])
	maxDiff = max(S)
	h = 1
	for i in range(len(localPeaks)):
		if S[i]>mean+h*std and localPeaks[i][1]>=maxPeak*0.40:
			significantPeaks.append(localPeaks[i])
	return significantPeaks


def getSignificantValleys(localValleys):
	significantValleys = []
	localValleys = []
	S = []
	
	k=1
	for i in range(len(dailyViewCount)):
		if i==0:
			x_left = dailyViewCount[i]
		else:
			x_left = min(dailyViewCount[max(0,i-k):i])
		if i==len(dailyViewCount)-1:
			x_right = dailyViewCount[i]
		else:
			x_right = min(dailyViewCount[i+1:min(i+k+1,len(dailyViewCount))])
		if dailyViewCount[i] < (x_left + x_right)/2.0 : 
			localValleys.append((i+1,dailyViewCount[i]))
			S.append(((dailyViewCount[i]-x_left) + (dailyViewCount[i]-x_right))/2.0)

	mean = np.mean(S)
	std = np.std(S)
	h = 1
	for i in range(len(localValleys)):
		if S[i]<mean+h*std:
			significantValleys.append(localValleys[i])
	return significantValleys



def getCategory(dailyViewCount):
	category = ['PeakInit','PeakMul','PeakLate','MonDec','MonIncr']
	peaks = getSignificantPeaks(dailyViewCount)
	valleys = getSignificantValleys(dailyViewCount)
	top05window = len(dailyViewCount)*0.05
	top10window = len(dailyViewCount)*0.10
	top30window = len(dailyViewCount)*0.30
	maxPeak = max([x[1] for x in localPeaks])
	if len(peaks)==0:
		return "Others"
	if peaks[len(peaks)-1][0] <=  top10window: #and all(earlier >= later for earlier, later in zip(dailyViewCount[int(top10window):], dailyViewCount[int(top10window)+1:])):
		return 'MonDec'
	elif peaks[len(peaks)-1][0] <= top30window:# and all(earlier >= later for earlier, later in zip(dailyViewCount[int(top25window):], dailyViewCount[int(top25window)+1:])):
		return 'PeakInit'
	elif len(peaks)<=10 and peaks[0][0]>top30window:# and all(earlier >= later for earlier, later in zip(dailyViewCount[peaks[0][0]:], dailyViewCount[peaks[0][0]+1:])):
		return 'PeakLate'
	elif all(np.diff(dailyViewCount)>=-maxPeak*0.2):#len(peaks)<top05window: #all(earlier <= later for earlier, later in zip(dailyViewCount, dailyViewCount[1:])):
		return 'MonoIncr'
	else:
		return 'PeakMul' 



def plot(views):
	x = [i+1 for i in range(len(views))]
	y = [i for i in views]
	plt.plot(x,y)
	plt.ylabel('View count')
	plt.xlabel('Day')
	plt.show()




 







videoIds = getVideoIds()
peaks = dict.fromkeys(videoIds,[])
valleys = dict.fromkeys(videoIds,[])
ofile = open('PeakCategory.csv','w')
writer = csv.writer(ofile)
writer.writerow(['VideoId','Peak Category','Peaks'])

for i in range(len(videoIds)):
	dailyViewCount = getDailyViewCount(videoIds[i])
	localPeaks = getLocalPeaks(dailyViewCount)
	significantPeaks = getSignificantPeaks(dailyViewCount)
	category = getCategory(dailyViewCount)
	# if category=='PeakLate':
	# 	print category
	# 	print significantPeaks
	# 	print 
	# 	print
	# 	plot(dailyViewCount)
	writer.writerow([videoIds[i],category,str(significantPeaks)])

ofile.close()




