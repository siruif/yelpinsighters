# Author: Sirui Feng
# This file generates a dictionary with information of similar users

import csv
import json
import time

#review_data_path = '../yelp_academic_dataset_review.json'
count_data_path = 'mr_output.csv'
review_data_path = 'test.json'

def user_pair_same_star_dict():
	pair_dict_zero = dict()
	pair_dict_five = dict()
	with open(count_data_path) as csvfile:
		r = csv.reader(csvfile, delimiter = ',')
		headers = next(r, None)
		for row in r:
			user_pair = row[0]
			cnt = row[1]
			user_pair = user_pair.split(",")
			u1 = user_pair[0][2:-1]
			u2 = user_pair[1][2:-2]
			pair_dict_five[(u1,u2)] = user_pair_helper(u1,u2, cnt, 0.5)
			pair_dict_zero[(u1,u2)] = user_pair_helper(u1,u2, cnt, 0)
	print("with threshold of zero:", pair_dict_zero)
	print("with threshold of 0.5:", pair_dict_five)
	print(pair_dict_five==pair_dict_zero)


def user_pair_helper(u1,u2, cnt, threshold_stars):
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
					star2=u2_helper(u2, business)
					if star2!=None and abs(star1-star2)<=threshold_stars:
						rv[business]=(star1, star2)

	return rv

def u2_helper(u2, business):
	with open(review_data_path) as review_data:
		for line in review_data:
			row = json.loads(line)
			user = row['user_id']
			b = row['business_id']
			if user == u2 and b == business:
				return row['stars']


user_pair_same_star_dict()