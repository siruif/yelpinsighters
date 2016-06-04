# Author: Sirui Feng

# This file generates a dictionary with information of similar users,
# calculates the proportion of users share similar tastes,
# and plot descriptive charts regarding similar users.

import csv
import json
import time

review_data_path = '../yelp_academic_dataset_review.json'
count_data_path = '../mr_user_pair.csv'
rate_output_path = 'output/similar_rate_results.csv'
gone_output_path = 'output/gone_same_results.csv'
overall_accuracy_output_path = 'output/overall_accuracy_results.txt'
proportion_output_path = 'output/proportion_results.csv'
accuracy_with_baseline_output_path = 'output/accuracy_with_baseline.csv'

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
	

	rv['accuracy'] = (rv['cnt_similar_busn_rate'])/(cnt_same_busn_gone)

	return rv

def gen_similar_taste_dict(threshold_stars, review_master_dict):
	'''
	Generates a dictionary -- similar_taste_dict

	similar_taste_dict = {(user1_id,user2_id):{ 'cnt_similar_busn_rate': 6,
	'cnt_same_busn_gone': 10, 
	'accuracy' = 0.6
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
		if similar_taste_dict[pair]['cnt_same_busn_gone'] >= num_busn:
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

def calculate_and_output_overall_accuracy(similar_taste_dict):
	with open(overall_accuracy_output_path, 'w') as f:
		accuracy_list=list()
		accuracy_sum = 0

		for pair in similar_taste_dict:
			accuracy = similar_taste_dict[pair]['accuracy']
			accuracy_list.append(accuracy)

		for a in accuracy_list:
			accuracy_sum += a

		overall_accuracy = accuracy_sum/len(accuracy_list)

		overall_accuracy =  "The average accuracy for the entire dataset is: " + str(round(overall_accuracy,2))

		print(overall_accuracy, file = f)

		return overall_accuracy

def calculate_and_output_accuracy_with_baseline(similar_taste_dict, baseline_list):
	with open(accuracy_with_baseline_output_path, 'w') as outfile:
		fieldnames = ['baseline', 'accuracy']
		writer = csv.DictWriter(outfile, fieldnames = fieldnames)
		writer.writeheader()
		for baseline in baseline_list:
			print("Calculating accuracy with a baseline of:", baseline)
			row = {}
			accuracy_list = list()
			for user_pair in similar_taste_dict:
				cnt_similar_busn_rate = similar_taste_dict[user_pair]['cnt_similar_busn_rate']
				cnt_same_busn_gone = similar_taste_dict[user_pair]['cnt_same_busn_gone']
				if cnt_similar_busn_rate >= baseline and cnt_same_busn_gone > baseline:
					a = (cnt_similar_busn_rate - baseline)/(cnt_same_busn_gone - baseline)
					accuracy_list.append(a)

			accuracy_sum=0
			for accuracy in accuracy_list:
				accuracy_sum += accuracy

			row['baseline'] = baseline
			row['accuracy'] = accuracy_sum/len(accuracy_list)

			writer.writerow(row)

if __name__ == '__main__':
	program_start_time = time.time()

	start_time = time.time()
	review_master_dict = read_json_to_dict(review_data_path)
	end_time = time.time()
	print("Converting from json to dictionary takes", end_time-start_time, "seconds")

	print("Generating similar_taste_dict...")
	start_time = time.time()
	threshold_stars = 0
	similar_taste_dict = gen_similar_taste_dict(threshold_stars, review_master_dict)
	end_time = time.time()
	print("Generating similarity dictionary takes", end_time-start_time, "seconds")
	print()

	# print("Writing results to csv files...")
	# write_results(similar_taste_dict)
	# print("Done writing to csvs")
	# print()

	start_time = time.time()
	print("Calculating accuracy with a baseline...")
	baseline_list = [2, 3, 4, 5, 6, 7]
	calculate_and_output_accuracy_with_baseline(similar_taste_dict, baseline_list)
	end_time = time.time()
	print("Calculating accuracy with a baseline takes", end_time-start_time, "seconds")
	print()

	print("Calculating overall accuracy...")
	start_time = time.time()
	overall_accuracy = calculate_and_output_overall_accuracy(similar_taste_dict)
	end_time = time.time()
	print("Calculating overall accuracy takes", end_time-start_time, 'seconds')
	print()

	print("Doing calculations regarding proportions...")
	start_time=time.time()
	given_same_num_busn_list = [2,3,4,5,6,7,8,9]
	fieldnames = ['given_same_num_busn', 'num_busn', 'proportion']
	with open(proportion_output_path, 'w') as f:
		writer = csv.DictWriter(f, fieldnames = fieldnames)
		writer.writeheader()
		row = {}

		for given_same_num_busn in given_same_num_busn_list:
			for num_busn in range(given_same_num_busn+1, 10):
				proportion = calculate_proportion(similar_taste_dict, given_same_num_busn, num_busn)
				row['given_same_num_busn'] = given_same_num_busn
				row['num_busn'] = num_busn
				row['proportion'] = proportion
				print("The probability of given user pair has rated", given_same_num_busn, \
				"businesses whithin a threshold of", threshold_stars, "the probability that they rate", num_busn, \
				'businesses similarly is', proportion)
				print("Writing this result to", proportion_output_path,"...")
				print()
				writer.writerow(row)
	end_time = time.time()
	print("Calculating proportions takes", end_time-start_time, 'seconds')


	program_end_time = time.time()
	print("The entire program takes", (program_end_time-program_start_time)/60, 'minutes')

	print("~"*70)
	print("High Five!")
