# Author: Sirui Feng
# This file generates a dictionary with information of similar users

import csv
import json
import time

review_data_path = '../yelp_academic_dataset_review.json'
count_data_path = 'mr_output.csv'

def user_pair_same_star_dict():
	pair_dict = dict()
	with open(count_data_path) as csvfile:
		r = csv.reader(csvfile, delimiter = ',')
		headers = next(r, None)
		for row in r:
			u1, u2 = row[0]
			cnt = row[1]
			pair_dict[(u1,u2)] = user_pair_helper(u1,u2, cnt)


def user_pair_helper(u1,u2, cnt):
	rv = dict()
	rv['cnt_same_bus'] = cnt
	with open(review_data_path) as review_data:
		for i in range(cnt):

			for line1 in review_data:
				row1 = json.loads(line1)
				user1 = row1['user_id']
				if user1 == u1:
					business = row1['business_id']
					star1 = row1['stars']
					for line2 in review_data:
						row2 = json.loads(line2)
						user2 = row2['user_id']
						if user2 = u2:
							stars2 = row2['stars']
							if row2['business_id'] == business:
								rv[business] = (stars1, stars2)
								i += 1
	return rv

user_pair_same_star_dict()