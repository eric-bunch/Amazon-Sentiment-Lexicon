from sys import argv

import string
import gzip
import collections
from collections import Counter, defaultdict
import math
import pickle
import random


script, genre = argv


def rev_num(index):
	return int(math.floor( index/11 ))
	
def rev_num_new(index):
	return int(math.floor( index/2 ))


def separate_reviews(g, revScH):
	
	reviews_files_list = []
	
	for score in range(1,6):
		reviews_files_list.append(gzip.open(g + '_%s.txt.gz' % score, 'wb'))
		
	with gzip.open(g + '.txt.gz', 'rb') as f:
		for index, line in enumerate(f):
			if (index % 11) == 9:
				for score in range(1, 6):
					if revScH[rev_num(index)] == score:
						reviews_files_list[score - 1].write(line[13:])
						reviews_files_list[score - 1].write('\n')
	
	for score in range(1,6):
		reviews_files_list[score - 1].close()
		
		
def separate_reviews_character_limit(g, revScH, char_limit):
	
	reviews_files_list = []
	reviewScoreHashCharLimit = {}
	
	for score in range(1,6):
		reviews_files_list.append(gzip.open(g + '_%s_%s_char_limit.txt.gz' % (score, char_limit), 'wb'))
		
	with gzip.open(g + '.txt.gz', 'rb') as f:
		for index, line in enumerate(f):
			if (index % 11) == 9 and len(line[13:]) <= 140:
				for score in range(1, 6):
					if revScH[rev_num(index)] == score:
						reviewScoreHashCharLimit[int(math.floor( index/11 ))] = score
						reviews_files_list[score - 1].write(line[13:])
						reviews_files_list[score - 1].write('\n')
	
	for score in range(1,6):
		reviews_files_list[score - 1].close()
	return reviewScoreHashCharLimit
		
	
def create_normalized_reviews(g, revScH, char_limit, percentage_build, percentage_train, percentage_test):
	if percentage_build + percentage_train + percentage_test != 1:
		return "Error: percentages do not add up to 100%"
		
	total = collections.Counter(revScH.values()).most_common()[-1][1]
	
	number_build = int(math.floor(total * percentage_build))
	number_train = int(math.floor(total * percentage_train))
	number_test = int(math.floor(total * percentage_test))
	
	total_length = range(0, total)
	random.shuffle(total_length)
	
	build_list = total_length[:number_build]
	train_list = total_length[number_build: number_build + number_train]
	test_list = total_length[number_build + number_train:]
	
	build = gzip.open(g + '_build.txt.gz', 'w')
	train = gzip.open(g + '_train.txt.gz', 'w')
	test = gzip.open(g + '_test.txt.gz', 'w')
	
	for score in range(1, 6):
		f = gzip.open(g + '_%s_%s_char_limit.txt.gz' % (score, char_limit), 'rb')
		for index, line in enumerate(f):
			if index % 2 == 0:
				if rev_num_new(index) in build_list:
					build.write(str(score))
					build.write('\t')
					build.write(line)
					build.write('\n')
				elif rev_num_new(index) in train_list:
					train.write(str(score))
					train.write('\t')
					train.write(line)
					train.write('\n')
				elif rev_num_new(index) in test_list:
					test.write(str(score))
					test.write('\t')
					test.write(line)
					test.write('\n')
	
	build.close()
	train.close()
	test.close()
		
		
reviewScoreHash = dict(map(lambda (k, v): (int(k), int(v)), 
							[line.split('\t') for line in open(genre + " review scores hash.tsv")] ))
	
separate_reviews(genre, reviewScoreHash)	
reviewScoresCharacterLimit = separate_reviews_character_limit(genre, reviewScoreHash, 140)
create_normalized_reviews(genre, reviewScoresCharacterLimit, 140, 0.3, 0.56, 0.14)



