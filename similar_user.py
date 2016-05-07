# Author: Sirui Feng
# This file generates a dictionary with information of similar users

import csv
import json
import time

review_data_path = '../yelp_academic_dataset_review.json'

def read_pair():
	with open('test.csv') as csvfile:
		r = csv.reader(csvfile, delimiter = ',')
		headers = next(r, None)
		for row in r:
			u1, u2 = row[0]
			simimlar_users(u1,u2)


def simimlar_users(u1,u2):
	with open(review_data_path) as review_data:
		for line in review_data:
			row = json.loads(line)
			business = row['business_id']