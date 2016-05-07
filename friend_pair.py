# Author: Sirui Feng, Turab Hassan
# This file generates friend pairs.

import json

user_data_path = '../yelp_academic_dataset_user.json'
review_data_path = '../yelp_academic_dataset_review.json'

def generate_pair():

	'''
	1.8 million friend pairs
	'''

	friend_pairs = set()
	cnt = 0
	user_set = set()
	with open(user_data_path) as data_file:
			for line in data_file:
				row = json.loads(line)
				user = row['user_id']
				user_set.add(user)


	with open(user_data_path) as data_file:
			for line in data_file:
				row = json.loads(line)
				user = row['user_id']
				friend_list = row['friends']
				for each in friend_list:
					if each in user_set:
						pair = (user, each)
						pair = tuple(sorted(pair))
						friend_pairs.add(pair)

	return friend_pairs

def same_place():
	friend_pair = generate_pair()
	rv= set()
	cnt=0
	stopper=0
	for each_pair in friend_pair:
		print(each_pair)
		user, friend = each_pair
		business = list()
		with open(review_data_path) as review_data:
			for line in review_data:
				row = json.loads(line)
				if row['user_id'] == user:
					print(row['business_id'])
					if find_business(row['business_id'], friend):
						cnt+=1
		break
	print(cnt)


					#business.append(row['business_id'])

def find_business(business_id, friend):
	with open(review_data_path) as review_data:
			for line in review_data:
				row = json.loads(line)
				if row['business_id'] == business_id and row['user_id']==friend:
					print("found business!")
					return True

same_place()


