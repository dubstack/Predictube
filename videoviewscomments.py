import os
import datetime
import time

def get_date_from_timestamp(tm):
	return datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.gmtime(int(tm)/1000.)),'%Y-%m-%d')

def write_day_views_comments_for_each_video(working_directory):
	output_dir=working_directory+'videoviewscomments/'
	dirs=os.listdir(working_directory+'Day wise views/views/')
	for file in dirs:
		print file
		view=open(working_directory+'Day wise views/views/'+file,'r')
		views=view.read().split('\n')[:-1]
		view.close()
		try:
			com=open(working_directory+'Comments Crawled/video_comments/'+file,'r')
			comm=com.read().split(file+'***||***')[1:]
			com.close()
			out=open(output_dir+file+'.txt','w')
			datepub=datetime.datetime.strptime(views[0].split()[-1],'%Y-%m-%d')
			print datepub
			ccnt=[0 for i in range(len(views))]
			for i in comm:
			    tm=i.split('***||***')[-1]
			    dt2=get_date_from_timestamp(tm)
			    day=(dt2-datepub).days
			    ccnt[day]+=1
			for i in views[1:]:
				out.write(i+'\t'+str(ccnt[int(i.split('\t')[0])-1])+'\n')
			out.close()
		except:
			try:
				out=open(output_dir+file+'.txt','w')
				datepub=datetime.datetime.strptime(views[0].split()[-1],'%Y-%m-%d')
				for i in views[1:]:
				    out.write(i+'\t0\n')
				out.close()
			except:
				pass

def main():
	working_directory='/home/bhushan/Documents/Soc_Comp_Project/youtube_data/'
	write_day_views_comments_for_each_video(working_directory)

if __name__=='__main__':
	main()