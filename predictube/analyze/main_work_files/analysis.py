import csv
import operator
import matplotlib.pyplot as plt

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

def plot_all_category_distribution(data,categories):
	dic_categories_all = {}
	dic_categories_ge = {}
	dic_categories_le = {}
	for cat in categories:
		dic_categories_le[cat] = 0
		dic_categories_ge[cat] = 0
		dic_categories_all[cat] = 0
	for row in data:
		val = int(row[-2])
		if val < 10:
			dic_categories_le[row[-3]] += 1
		else :
			dic_categories_ge[row[-3]] += 1
		dic_categories_all[row[-3]] += 1

	sorted_dic = sorted(dic_categories_all.items(),reverse=True, key=operator.itemgetter(1))
	x = [i+1 for i in range(len(categories))]
	y_all = [val for key,val in sorted_dic]
	total_videos = sum(y_all)
	y_all = [val*100.0/total_videos for val in y_all]
	labels = [key for key,val in sorted_dic]
	total_videos = sum(dic_categories_ge.values())
	y_ge = [dic_categories_ge[label]*100.0/total_videos for label in labels]
	total_videos = sum(dic_categories_le.values())
	y_le = [dic_categories_le[label]*100.0/total_videos for label in labels]
	plt.margins(0.05)
	plt.title("Distribution of videos in various categories")
	plt.xlabel("Categories")
	plt.ylabel("Percentage of total videos")

	plt.plot(x, y_all, label="all videos")
	plt.plot(x, y_ge, label="atleast 10 Comments")
	plt.plot(x, y_le, label="less than 10 Comments")
	plt.legend(loc="upper right")
	plt.xticks(x, labels, rotation="vertical")
	plt.show()

def plot_category_distribution(data,categories):
	dic_categories = {}
	for cat in categories:
		dic_categories[cat] = 0
	counter = 0
	for row in data:
		if int(row[-2]) < 10:
			counter += 1
			dic_categories[row[-3]] += 1
	print counter
	sorted_dic = sorted(dic_categories.items(),reverse=True, key=operator.itemgetter(1))
	x = [i+1 for i in range(len(categories))]
	y = [val for key,val in sorted_dic]
	total_videos = sum(y)
	y = [val*100.0/total_videos for val in y]
	labels = [key for key,val in sorted_dic]
	plt.margins(0.05)
	plt.title("Distribution of videos in various categories")
	plt.xlabel("Categories")
	plt.ylabel("Percentage of total videos")

	plt.bar(x, y)
	plt.xticks(x, labels, rotation="vertical")
	plt.show()

def run(dir_path):
	# dir_path_comments = dir_path + "youtube_data/Comments Crawled/video_comments/"
	# dir_path_views = dir_path + "youtube_data/Day wise views/views/"
	file_path = dir_path + "MasterData.csv"
	header, data = get_all_data(file_path)
	categories = get_all_categories(data)
	# plot_category_distribution(data, categories)
	plot_all_category_distribution(data, categories)
def main():
	dir_path = "/Users/bp/Projects/SocialComputing/"
	run(dir_path)

if __name__ == '__main__':
	main()