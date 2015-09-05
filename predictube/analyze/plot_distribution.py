import csv
import matplotlib.pyplot as plt
def main():
	file_path = "superwoman_statistics.csv"
	f = open(file_path,"r")
	reader = csv.reader(f)
	line_num = 0
	data = []
	header = ""
	for row in reader:
		if line_num == 0:
			header = row
		else :
			data.append(row)
		line_num += 1
	print header
	fraction = []
	for video in data :
		if video[6] != "[]":
			view_count_cumulative = map(int,video[8][1:-1].split(", "))
			subscriber_cumulative = map(int,video[6][1:-1].split(", "))
			print subscriber_cumulative[:10]
			print view_count_cumulative[:10]
			print "Aaquib"
			# fraction.append(float(subscriber_cumulative)/view_count_cumulative)
	fraction = map(lambda x: x*100, fraction)
	fraction = sorted(fraction)
	plt.plot(fraction)
	plt.show()

if __name__ == '__main__':
	main()