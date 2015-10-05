from bs4 import BeautifulSoup
import re
import requests
import sys
import time
import codecs
from sentimentAnalysis import averageSentimentScore
def crawl(counter,url):
	f = codecs.open("data/cam_"+str(counter)+".xml",'w','utf-8')
	f.write("<specsKey=\"link\">"+url.strip(" \n\r\t")+"</specsKey>\n")
	for x in range(1,1000):
		try:
			page_1 = requests.get(url)
			break
		except:
			time.sleep(1)
	soup = BeautifulSoup(page_1.text)
	try:
		averageRating=str(soup.find("div", {"class":"bigStar"}).text).strip()
	except:
		averageRating=""
		print "AvgRatingFailed"
	try:
		ratingCount=soup.find("div", {"class":"ratingHistogram"})
		ratingCount=ratingCount.findAll("p",{"class":"subText"})[1].text
		ratingCount= re.findall('\d+', ratingCount )[0]
	except:
		ratingCount=""
		print "RatingCountFailed"

	try:
		imgUrl =str(soup.find("div", {"class":"imgWrapper"}).contents[1]['data-src']).strip()
	except:
		imgUrl=""
	try:
		price = str(soup.find("span", {"class":"selling-price omniture-field"})["data-evar48"]).strip()
	except:
		price=""
	try:
		titler = str(soup.find("h1", {"class":"title"},{"itemprop":"name"}).contents[0]).strip()
	except:
		titler=""
	reviewCount=""
	reviews=[]
	try:
		titles =soup.find("div", {"class":"helpfulReviews"})
		link= titles.find("a")
		reviewCount = re.findall('\d+', link.text)[0]
		link=link['href']
		link="http://www.flipkart.com"+link
		for x in range(1,1000):
			try:
				page_2 = requests.get(str(link))
				break
			except:
				time.sleep(1)
		
		soup2 = BeautifulSoup(page_2.text)
		titles =soup2.findAll("span", {"class":"review-text"})
		counte=0
		for title in titles:
			counte+=1
			review=title.text
			review=review.replace("\n"," ")
			reviews.append(review)
			if(counte==10):
				break
	except:
		pass
	sentimentScore=averageSentimentScore(reviews)
	specsKey = []
	specsValue = []
	try:
		specsKey = soup.find("div", {"class": "productSpecs specSection"}).findAll("td", {"class": "specsKey"})
		specsValue = soup.find("div", {"class": "productSpecs specSection"}).findAll("td", {"class": "specsValue"})
	except:
		pass

	f.write("<specsKey=\"avg_rating\">"+averageRating+"</specsKey>\n")
	f.write("<specsKey=\"number_of_ratings\">"+ratingCount+"</specsKey>\n")
	f.write("<specsKey=\"number_of_reviews\">"+reviewCount+"</specsKey>\n")
	f.write("<specsKey=\"img_url\">"+imgUrl+"</specsKey>\n")
	f.write("<specsKey=\"price\">"+price+"</specsKey>\n")
	f.write("<specsKey=\"title\">"+titler+"</specsKey>\n")
	f.write("<specsKey=\"sentiment_score\">"+str(sentimentScore)+"</specsKey>\n")
	for x in range(len(specsKey)):
		if specsKey[x].text=="Color":
			f.write("<specsKey=\""+specsKey[x].text.lower()+"\">"+specsValue[x].text.strip(" \n\r\t")+"</specsKey>\n")
	for x in range(len(specsKey)):
		if specsKey[x].text=="Type":
			f.write("<specsKey=\""+specsKey[x].text.lower()+"\">"+specsValue[x].text.strip(" \n\r\t")+"</specsKey>\n")
	for i in range(len(reviews)):
		f.write("<specsKey=\"review"+str(i+1)+"\">"+reviews[i].strip(" \n\r\t")+"</specsKey>\n")

	for x in range(len(specsKey)):
		if not (specsKey[x].text=="Color" or specsKey[x].text=='Type') :
			f.write("<specsKey=\""+specsKey[x].text+"\">"+specsValue[x].text.strip(" \n\r\t")+"</specsKey>\n")

def main():
	lines = [line.strip() for line in open('urls.txt')]
	counter=0
	for line in lines:
		crawl(counter,line)
		print counter
		counter+=1

if __name__ == '__main__':
	main()
