# Author: Sirui Feng

# This file generates a dictionary with information of similar users,
# calculates the proportion of users share similar tastes,
# and plot descriptive charts regarding similar users.

import csv
import json
import time

review_data_path = '../yelp_academic_dataset_review.json'
count_data_path = 'mr_user_pair.csv'
#review_data_path = 'test.json'
rate_output_path = 'similar_rate_results.csv'
gone_output_path = 'gone_same_results.csv'

def read_json_to_dict(review_data_path):
	'''
	Generates review_master_dict that stores information of review dataset.
	Reads in the json file and stores it as a dictionary as the following format--
	review_master_dict={user1_id: {business1_id:{'review_id':'abc', 'stars' = 4}, 
	business2_id:{'review_id':'abc', 'stars' = 4}, user2_id:...}

	'''
	review_master_dict = dict()
	with open(review_data_path) as review_data:
		for line in review_data:
			row = json.loads(line)
			review_id = row['review_id']
			stars = row['stars']
			user_id = row['user_id']
			business_id = row['business_id']
			if user_id not in review_master_dict:
				review_master_dict[user_id] = dict()
				review_master_dict[user_id][business_id] = {"review_id":review_id, "stars": stars}
			else:
				review_master_dict[user_id][business_id] = {"review_id":review_id, "stars" : stars}

	return review_master_dict

# def u2_helper(u2, business, review_master_dict):
# 	'''
# 	Returns the stars corresponding with user_id: u2 and business_id: business
# 	'''
# 	for review in review_master_dict:
# 		user = review_master_dict[review]['user_id']
# 		b = review_master_dict[review]['business_id']
# 		if (user == u2) and (b == business):
# 			stars = review_master_dict[review]['stars']
# 			return stars

	# with open(review_data_path) as review_data:
	# 	for line in review_data:
	# 		row = json.loads(line)
	# 		user = row['user_id']
	# 		b = row['business_id']
	# 		if (user == u2) and (b == business):
	# 			return row['stars']

def user_pair_helper(u1, u2, cnt_same_busn_gone, threshold_stars, review_master_dict):
	'''
	Generates for each user pair u1 and u2: { 'cnt_similar_busn_rate': 6,
	'cnt_same_busn_gone': 10...}
	'''
	rv = dict()
	rv['cnt_same_busn_gone'] = cnt_same_busn_gone
	rv['cnt_similar_busn_rate'] = 0
	business_set = set()
	for business in review_master_dict[u1]:
		business_set.add(business)
	for b in business_set:
		if b in review_master_dict[u2]:
			stars1 = review_master_dict[u1][b]['stars']
			stars2 = review_master_dict[u2][b]['stars']
			if abs(stars1-stars2) <= threshold_stars:
				rv['cnt_similar_busn_rate'] += 1

		

	# with open(review_data_path) as review_data:
	# 	for line1 in review_data:
	# 		row1 = json.loads(line1)
	# 		user = row1['user_id']
	# 		if user == u1:
	# 			business = row1['business_id']
	# 			if business not in business_set:
	# 				business_set.add(business)
	# 				star1 = row1['stars']
	# 				star2 = u2_helper(u2, business)
	# 				if star2 != None and abs(star1-star2) <= threshold_stars:
	# 					rv['cnt_similar_busn_rate'] += 1

	return rv

def gen_similar_taste_dict(threshold_stars, review_master_dict):
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
		i=1
		
		for row in r:
			cnt_same_busn_gone = int(row[1])

			user_pair = row[0]
			user_pair = user_pair.split(",")
			u1 = user_pair[0][3:-1]	#slice beacuase of the parantheses
			

			u2 = user_pair[1][3:-2]	#slice beacuase of the parantheses

			similar_taste_dict[(u1,u2)] = user_pair_helper(u1, u2, cnt_same_busn_gone, threshold_stars, review_master_dict)
			print(i, 'out of 15924491 entries done...')
			i+=1

	return similar_taste_dict
	
def calculate_proportion(similar_taste_dict, given_same_num_busn, num_busn):
	'''
	This function returns the proportion of the total number of user 
	pairs who rated given_same_num_busn similarly, the proportion of them
	rated num_busn similarly
	'''
	assert given_same_num_busn <= num_busn

	d = 0
	n = 0

	for pair in similar_taste_dict:
		if similar_taste_dict[pair]['cnt_similar_busn_rate'] >= given_same_num_busn:
			d += 1
			if similar_taste_dict[pair]['cnt_similar_busn_rate'] >= num_busn:
				n += 1

	return n/d

def write_dict_to_csv(dictionary, fieldnames, output_path):
	'''
	Writes a dictionary's fieldnames into a csv file by using DictWriter of csv writer.

	https://docs.python.org/3/library/csv.html
	'''
	with open(output_path, 'w') as outfile:
		writer = csv.DictWriter(outfile, fieldnames = fieldnames)
		
		writer.writeheader()
		for user_pair in dictionary:
			row = dict()
			row['user_pair'] = user_pair
			for field in fieldnames:
				if field != 'user_pair':
					row[field] = dictionary[user_pair][field]
			writer.writerow(row)

def write_results(similar_taste_dict):
	write_dict_to_csv(similar_taste_dict, ['user_pair', 'cnt_similar_busn_rate'], rate_output_path)
	write_dict_to_csv(similar_taste_dict, ['user_pair', 'cnt_same_busn_gone'], gone_output_path)

if __name__ == '__main__':
	start_time = time.time()
	review_master_dict = read_json_to_dict(review_data_path)
	end_time = time.time()
	print("Converting from json to dictionary takes", end_time-start_time, "seconds")

	threshold_stars = 0.5

	print("Generating similar_taste_dict...")

	start_time = time.time()
	similar_taste_dict = gen_similar_taste_dict(threshold_stars, review_master_dict)
	end_time = time.time()
	print("Generating similarity dictionary takes", end_time-start_time, "seconds")

	print()

	print("Writing results to csv files...")
	write_results(similar_taste_dict)
	print("Done writing to csvs")

	given_same_num_busn_list = [2,3,4,5,6,7,8,9]

	print("Doing calculations...")

	for given_same_num_busn in given_same_num_busn_list:
		for num_busn in range(given_same_num_busn+1, 10):
			proportion = calculate_proportion(similar_taste_dict, given_same_num_busn, num_busn)
			
			print("The probability of given user pair has rated", given_same_num_busn, \
			"businesses whithin a threshold of", threshold_stars, "the probability that they rate", num_busn, \
			'businesses similarly is', proportion)
	

	print("~"*70)
	print("High Five!")