# Author: Sirui Feng

# This file generates a dictionary with information of similar users,
# calculates the proportion of users share similar tastes,
# and plot descriptive charts regarding similar users.

import csv
import json
import time

review_data_path = '../yelp_academic_dataset_review.json'
count_data_path = 'mr_output.csv'
#review_data_path = 'test.json'


def u2_helper(u2, business):
	with open(review_data_path) as review_data:
		for line in review_data:
			row = json.loads(line)
			user = row['user_id']
			b = row['business_id']
			if (user == u2) and (b == business):
				return row['stars']

def user_pair_helper(u1,u2, cnt_same_busn_gone, threshold_stars):
	'''
	Generates for each user pair u1 and u2: { 'cnt_similar_busn_rate': 6,
	'cnt_same_busn_gone': 10, 
	business1_id: (star_ratings_user1, star_ratings_user2), 
	business2_id: (star_ratings_user1, star_ratings_user2), 
	business3_id: (star_ratings_user1, star_ratings_user2) 
	...
	business10_id: (star_ratings_user1, star_ratings_user2)}
	'''
	rv = dict()
	business_set = set()
	rv['cnt_same_busn_gone'] = cnt_same_busn_gone
	rv['cnt_similar_busn_rate'] = 0
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
						rv['cnt_similar_busn_rate'] += 1

	return rv

def gen_similar_taste_dict(threshold_stars):
	'''
	Generates a dictionary -- similar_taste_dict

	similar_taste_dict = {(user1_id,user2_id):{ 'cnt_similar_busn_rate': 6,
	'cnt_same_busn_gone': 10, 
	business1_id: (star_ratings_user1, star_ratings_user2), 
	business2_id: (star_ratings_user1, star_ratings_user2), 
	business3_id: (star_ratings_user1, star_ratings_user2) 
	...
	business10_id: (star_ratings_user1, star_ratings_user2)
	...}

	'''
	similar_taste_dict = dict()
	d = 0
	n = 0

	with open(count_data_path) as csvfile:
		r = csv.reader(csvfile, delimiter = ',')
		headers = next(r, None)	#skip the first row of header
		
		for row in r:
			cnt_same_busn_gone = int(row[1])

			user_pair = row[0]
			user_pair = user_pair.split(",")
			u1 = user_pair[0][2:-1]	#slice beacuase of the parantheses
			u2 = user_pair[1][2:-2]	#slice beacuase of the parantheses

			similar_taste_dict[(u1,u2)] = user_pair_helper(u1,u2, cnt_same_busn_gone, threshold_stars)

	return similar_taste_dict
	
def calculate_proportion(similar_taste_dict, given_same_num_busn, num_busn):
	'''
	This function returns the proportion of the total number of user 
	pairs who rated given_same_num_busn similarly, the proportion of them
	rated num_busn similarly
	'''
	assert given_same_num_busn<=num_busn

	d = 0
	n = 0

	for pair in similar_taste_dict:
		if similar_taste_dict[pair]['cnt_similar_busn_rate'] >= given_same_num_busn:
			d += 1
			if similar_taste_dict[pair]['cnt_similar_busn_rate'] >= num_busn:
				n += 1

	return n/d

if __name__ == '__main__':
	similar_taste_dict = gen_similar_taste_dict(0.5)
	proportion = calculate_proportion(similar_taste_dict, 1, 3)
	print(proportion)