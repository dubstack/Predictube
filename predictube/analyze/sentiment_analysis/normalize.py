import re,sys,string
from nltk.corpus import stopwords
from spell import correct
from nltk.stem.lancaster import LancasterStemmer

stop_words = set(stopwords.words('english'))

stemmer = LancasterStemmer()

# unicodify(): will encode text as per unicode format
def unicodify(word):
	return word.encode('utf-8')

def tolower(word):
	return word.lower()

# goodify(): will remove characters in a word that occur more than three two times
def goodify(word):
	a = '$'
	b = '$'
	c = '$'
	ret = ''
	for x in word:
		a = b
		b = c
		c = x
		if a==b and b==c:
			continue
		else:
			ret+=x
	return ret

#clean(): Removes all punctuations and newlines, returns list of words.
def tokenize(text):
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	text = regex.sub('', text)
	return text.split()

#normalize(): main driver function
def normalize(text):
	# text = unicodify(text)o
	text = tokenize(text)
	return sanitize(text)

# #stem(): does Stemming + Correct , so as to get stemmed word which actually lies in the dictionary
# def stem(word):
# 	# word = stemmer.stem(word)
# 	word = correct(word)
# 	return word

#########
# sanitize():
# 1. Converts to lowercase
# 2. goodifies words
# 3. Removes Stop-Words
# 4. Spell-Corrects the word
# 5. Again checks for possible stop-words
##########
def sanitize(text):
	ret = []
	for word in text:
		word = tolower(word)
		word = goodify(word)
		word = correct(word)
		if word not in stop_words:
			ret.append(word)
		else:
			continue
	return ret
def main():
	st = 'Hi!!!  and but not in Im reaaally Haaaapppy  :P :D :) :-o \n \n :: :D 231414 so happy! &amp \n'
	print normalize(st)

if __name__ =='__main__':
	main()
