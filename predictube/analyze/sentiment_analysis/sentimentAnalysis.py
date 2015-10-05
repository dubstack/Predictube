import nltk
import codecs
from nltk.corpus import wordnet as wn
from normalize import *
def sentiReadWord(filename):
	dic={}
	lines = codecs.open(filename, "r", "utf8").read().splitlines()
	lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
	for i, line in enumerate(lines):
		fields = re.split(r"\t+", line)
		fields = map(unicode.strip, fields)
		pos, offset, pos_score, neg_score, synset_terms, gloss = fields
		if pos and offset:
			offset = int(offset)
			dic[(pos,offset)] = (float(pos_score), float(neg_score))
	return dic

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return ''

def sentiCalculateSentiment(listOfTokens,sentiDictionary):
	score=0
	listOfTokens = nltk.pos_tag(listOfTokens)
	for token in listOfTokens:
		# print "safdasdddddddddddddddddddddddddddddddddd"
		# print token
		negScore=0
		posScore=0
		tag=get_wordnet_pos(token[1])
		synset_list = wn.synsets(token[0])
		for synset in synset_list:
			pos = synset.pos()
			offset = synset.offset()
			if (pos, offset) in sentiDictionary:
				pos_score, neg_score = sentiDictionary[(pos, offset)]
				# print synset
				# print pos_score,neg_score
				if pos_score>neg_score:
					posScore+=1
				elif neg_score>pos_score:
					negScore+=1
		if negScore>posScore:
			score= score-1
		elif negScore<posScore:
			score+=1
		# print token, score
	if score>0:
		return 1
	elif score==0:
		return 0
	else:
		return -1

def calculate(review,sentiDictionary):
	listOfTokens=normalize(review)
	return sentiCalculateSentiment(listOfTokens,sentiDictionary)

def averageSentimentScore(reviews):
	if len(reviews)==0:
		return 0
	sentiDictionary=sentiReadWord('SentiWordNet_3.0.0_20100705.txt')
	total=float(len(reviews))
	sumi=0
	for review in reviews:
		sumi+=calculate(review,sentiDictionary)
	return sumi/total

def main():
	reviews=['happy bad unsatisfactory beautifu shit good awesome satisfied']
	print averageSentimentScore(reviews)
if __name__ == '__main__':
	main()