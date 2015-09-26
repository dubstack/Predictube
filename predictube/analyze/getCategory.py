import os

def getCategory(videoID):
	dir='categorybased/'
	dirs=os.listdir(dir)
	for fl in dirs:
		f=open(dir+fl,'r')
		vdos=f.read().split('\n')
		f.close()
		if videoID in vdos:
			return fl.split('.')[0]
	return ''
