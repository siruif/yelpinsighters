# Sirui Feng
# This file generates all pairs who have gone to same restaurant.
# First run this file, then similar_user.py


import json
import csv
import time
import itertools

review_data_path = 'all_review.json'	#test data
#review_data_path = '../yelp_academic_dataset_review.json'
#public_review_data_path = '../textinsighters/data/public_utilities.json'
user_pairs_outfile = 'user_pair.csv'


def read_reviews():
	'''
	Reads in the yelp reviews json file and generates dictionary.
	'''
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
	#print("There are ", len(reviews_dict), "unique business in review dataset")
	#print(reviews_dict)
	return reviews_dict

def generate_user_pair(reviews_dict):
	'''
	Generates user pair and outputs to a csv file.
	'''
	# business_dict records for each business, all the pairs who have gone to it
	# key is business_id, value is a list of tuples in the form of (user1,user2)
	with open(user_pairs_outfile, 'w') as outfile:
		w = csv.writer(outfile, delimiter = ',')
		w.writerow(['pair', 'business_id'])

		for business in reviews_dict:
			users = reviews_dict[business]
			#itertools generates a list of tuples
			for pair in itertools.combinations(users, 2):
			    w.writerow([pair,business])

def go():
	reviews_dict = read_reviews()
	start_time = time.time()
	generate_user_pair(reviews_dict)
	end_time = time.time()
	#print("generate_user_pair takes", end_time-start_time,"seconds")

go()
