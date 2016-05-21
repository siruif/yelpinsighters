# Author: Sirui Feng
# This file generates a dictionary with information of similar users

import csv
import json
import time

#review_data_path = '../yelp_academic_dataset_review.json'
count_data_path = 'mr_output.csv'
review_data_path = 'test.json'

def proportion_similar_tastes(threshold_stars, given_same_num_busn):
	'''
	This function returns the proportion of the total number of user 
	pairs who rated given_same_num_busn similarly, the proportion of them
	rated given_same_num_busn+1 similarly


	pair_dict_threshold = {(user1_id,user2_id):{ 'cnt_same_busn_review': 3, 
	business1_id: (star_ratings_user1, star_ratings_user2), 
	business2_id: (star_ratings_user1, star_ratings_user2), 
	business3_id: (star_ratings_user1, star_ratings_user2)}}
	'''
	pair_dict_threshold = dict()
	d = 0
	n = 0

	with open(count_data_path) as csvfile:
		r = csv.reader(csvfile, delimiter = ',')
		headers = next(r, None)	#skip the first row of header
		for row in r:
			num_total_pair += 1
			user_pair = row[0]
			cnt = row[1]
			user_pair = user_pair.split(",")
			u1 = user_pair[0][2:-1]
			u2 = user_pair[1][2:-2]
			pair_dict_threshold[(u1,u2)] = user_pair_helper(u1,u2, cnt, threshold_stars)
	
	print("with threshold of:",threshold_stars, "the pair_dict_threshold is:" pair_dict_threshold)

	for pair in pair_dict_threshold:
		if pair_dict_threshold[pair]['cnt_same_busn_review'] >= given_same_num_busn:
			d += 1
			if pair_dict_threshold[pair]['cnt_same_busn_review'] >= (given_same_num_busn+1):
				n += 1
	return n/d

def user_pair_helper(u1,u2, cnt, threshold_stars):
	'''
	Generates for each user pair u1 and u2: {'cnt_same_busn_review': 3, 
	business1_id: (star_ratings_user1, star_ratings_user2), 
	business2_id: (star_ratings_user1, star_ratings_user2), 
	business3_id: (star_ratings_user1, star_ratings_user2)}
	'''
	print('users are', u1,u2)
	rv = dict()
	business_set = set()
	rv['cnt_same_busn_review'] = int(cnt)
	with open(review_data_path) as review_data:
		for line1 in review_data:
			row1 = json.loads(line1)
			user = row1['user_id']
			if user == u1:
				business = row1['business_id']
				if business not in business_set:
					business_set.add(business)
					star1 = row1['stars']
					star2 = u2_helper(u2, business)
					if star2 != None and abs(star1-star2) <= threshold_stars:
						rv[business] = (star1, star2)

	return rv

def u2_helper(u2, business):
	with open(review_data_path) as review_data:
		for line in review_data:
			row = json.loads(line)
			user = row['user_id']
			b = row['business_id']
			if (user == u2) and (b == business):
				return row['stars']

proportion_similar_tastes(0.5, 2)