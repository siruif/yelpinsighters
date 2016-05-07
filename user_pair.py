# Sirui Feng
# This file generates all pairs who have gone to same restaurant.


import json
import csv
import time
import itertools

review_data_path = 'test.json'	#test data
#review_data_path = '../yelp_academic_dataset_review.json'
#public_review_data_path = '../textinsighters/data/public_utilities.json'
user_pairs_outfile = 'user_pairs.csv'


def read_reivews():
	# reviews_dict keeps track of the business and users who have gone to it
	# key is business_id, value is a set of users who have visted
	reviews_dict = dict()
	with open(review_data_path) as review_data:
		for line in review_data:
			row = json.loads(line)
			business = row['business_id']
			user = row['user_id']
			if business in reviews_dict:
				reviews_dict[business].add(user)
			else:
				reviews_dict[business] = set()
				reviews_dict[business].add(user)
	print("There are ", len(reviews_dict), "unique business in review dataset")
	print(reviews_dict)
	return reviews_dict

def generate_user_pair(reviews_dict):
	# business_dict records for each business, all the pairs who have gone to it
	# key is business_id, value is a list of tuples in the form of (user1,user2)
	with open(user_pairs_outfile, 'w') as outfile:
		w = csv.writer(outfile, delimiter = ',')
		w.writerow(['pair', 'business_id'])

		for business in reviews_dict:
			users = reviews_dict[business]
			#itertools generates a list of tuples
			user_pairs = list(itertools.combinations(users, 2))
			for pair in user_pairs:
				w.writerow([pair,business])

def go():
	reviews_dict = read_reivews()
	start_time = time.time()
	generate_user_pair(reviews_dict)
	end_time = time.time()
	print("generate_user_pair takes", end_time-start_time,"seconds")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

go()