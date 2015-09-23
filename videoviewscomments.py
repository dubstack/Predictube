import os
import datetime
import time
working_directory='/home/bhushan/Documents/Soc_Comp_Project/youtube_data/'
output_dir=working_directory+'videoviewscomments/'
dirs=os.listdir(working_directory+'Day wise views/views/')
for file in dirs:
	print file
	view=open(working_directory+'Day wise views/views/'+file,'r')
	try:
		com=open(working_directory+'Comments Crawled/'+file,'r')
		comm=com.read().split(file+'***||***')[1:]
		views=view.read().split('\n')[:-1]
		com.close()
		view.close()
		out=open(output_dir+file+'.txt','w')
		datepub=datetime.datetime.strptime(views[0].split()[-1],'%Y-%m-%d')
		ccnt=[0 for i in range(len(views)-1)]
		for i in comm:
		    tm=i.split('***||***')[-1]
		    dt2=datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.gmtime(int(tm)/1000.)),'%Y-%m-%d')
		    day=(dt2-datepub).days
		    ccnt[day]+=1
		for i in views[1:]:
		    out.write(i+'\t'+str(ccnt[int(i.split()[0])-1])+'\n')
		out.close()
	except:
		views=view.read().split('\n')[:-1]
		view.close()
		try:
			out=open(output_dir+file+'.txt','w')
			datepub=datetime.datetime.strptime(views[0].split()[-1],'%Y-%m-%d')
			ccnt=[0 for i in range(len(views)-1)]
			for i in views[1:]:
			    out.write(i+'\t0\n')
			out.close()
		except:
			pass