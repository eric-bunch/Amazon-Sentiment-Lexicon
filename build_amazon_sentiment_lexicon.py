from sys import argv

import string
import gzip
import collections
from collections import Counter, defaultdict
import math

# Natural language processing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def build_amazon_sent_hash(g):
	
	amazonSentHash = defaultdict(lambda: [], {})
	
	stop_words = set(stopwords.words("english"))
	
	with gzip.open(g + '_build.txt.gz', 'rb') as f:
		for index, line in enumerate(f):
			if index % 2 == 0:
				text = line.split('\t')[1]
				score = int(line.split('\t')[0])
			
				if len(text) <= 140:
					review_text = [w.lower() for w in word_tokenize(text) 
												if w.isalpha() and not w in stop_words]
		
					for word in review_text:
						amazonSentHash[word].append(score)
						
		for word in amazonSentHash.keys():
			amazonSentHash[word] = collections.Counter(amazonSentHash[word]).most_common(1)[0][0]
			
	return amazonSentHash
												
	
def write_lexicon(sentimentHash, g, name):
	with open(g + " " + name + ".tsv", "w") as f: 	
		for word in sentimentHash:
			f.write(word)
			f.write('\t')
			f.write(str(sentimentHash[word]))
			f.write('\n')


script, genre = argv

reviewScoreHash = dict(map(lambda (k, v): (int(k), int(v)), 
							[line.split('\t') for line in open(genre + " review scores hash.tsv")] ))

amazonSentHash = build_amazon_sent_hash(genre)
write_lexicon(amazonSentHash, genre, "amazon sentiment lexicon")


