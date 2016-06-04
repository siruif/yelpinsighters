# Algorithm to identify business pairs who share the same categories
# Vi Nguyen, Sirui Feng, Turab Hassan

import json
import pandas as pd 
import csv
import time
import itertools
from similar_user import similar_taste_dict_with_category


def read(filename, file_format, json_obj_top_level_id = None):

	df = []
	if file_format == 'csv':
		df = pd.read_csv(filename)
	elif file_format == 'json objects':

		with open(filename) as data_file:
			data_dict = {}

			for line in data_file:
				row = json.loads(line)
				top_id_val = row.pop(json_obj_top_level_id, None)
				data_dict[top_id_val] = row
		df = pd.DataFrame.from_dict(data_dict, orient = "index")
		# resets df index to integers, instead of the top_id_val
		df = df.reset_index().rename(columns={"index": json_obj_top_level_id})
	else:
		print('the current file format is not supported')

	return df


def busn_category_pair(filename):

	df = read(filename, "json objects", "business_id")

	cat_count_dict = {}

	for categories in df['categories']:
		for cat in categories:
			cat_count_dict[cat] = cat_count_dict.setdefault(cat, 0) + 1

	cat_busn_dict = {}
	for key, val in cat_count_dict.items():
		if val > 2:
			for i in range(len(df)):
				if key in df['categories'][i]:
					cat_busn_dict[key] = cat_busn_dict.setdefault(key, set())
					cat_busn_dict[key].add(df['business_id'][i])
	
	
	return cat_count_dict, df, cat_busn_dict


def generate_similar_pairs(dictname, outfilename, pairname, similarity_id):
	# business_dict records for each business, all the pairs who have gone to it
	# key is business_id, value is a list of tuples in the form of (user1,user2)
	
	#with open(outfilename, 'w', newline = '') as outfile:
	#	w = csv.writer(outfile, delimiter = ',')
	#	w.writerow([pairname, similarity_id])

	pairs_busn_cat = {}

	for val in dictname:
		in_set = sorted(dictname[val])
		#itertools generates a list of tuples
		for pair in itertools.combinations(in_set, 2):
			pairs_busn_cat[pair] = val

	return pairs_busn_cat


def accuracy_with_cat_baseline(pairs_busn_cat, dict_cat, dict_user_pairs):
	# pairs_busn_cat - csv file name that holds the info on pairs of businesses that share a given category, comes in the form of [(busn1, busn2), category]
	# dict_cat - dictionary of categories where key is category, and value is a set of all the businesses that shared that category
	# dict_user_pairs - dictionary of where key is a pair of user, and value is a tuple of list of busineses that the pair has gone to, and a list of tuples of businesses that the pairs have rated the same
	# {(u1,u2): {'busn_list':[b1, b2, b3, b4], 'similar_rate_busn_pair': [(b1,b2), (b2, b3), (b1,b3)]}, (u2,u3):{}...}

	accuracy = []
	sim_rate = set()
	counted_ind = 0

	for u_pair in dict_user_pairs:
		for busn_pair in dict_user_pairs[u_pair]:
			for val in busn_pair:
				sim_rate.add(val)

	for u_pair in dict_user_pairs:
		count_gone = 0
		count_sim_rate = 0
		for b_pair in dict_user_pairs[u_pair]['similar_rate_busn_pair']:
			category = set()
			if b_pair in pairs_busn_cat:
				category.add(pairs_busn_cat[b_pair])
			for busn in dict_user_pairs[u_pair]['busn_list']:
				if busn not in b_pair:
					for cat in category:
						if busn in dict_cat[cat]:
							count_gone = count_gone + 1
							counted_ind = 1
						if busn in sim_rate:
							count_sim_rate = count_sim_rate + 1
							counted_ind = 1
					if counted_ind != 0: # only wants to count a busn once
						break
			print("u_pair: {}\n b_pair: {} \n category: {} \n count_gone: {} \n count_sim_rate: {} \n")
		accuracy_rate = (sum(count_sim_rate)/len(count_sim_rate))
		accuracy.append(accuracy_rate)

	print("accuracy:", accuracy)
	overall_accuracy = sum(accuracy) / len(accuracy)


if __name__ == '__main__':
	print("initializing...")
	start_time = time.time()
	cat_count_dict, df, cat_busn_dict = busn_category_pair("datafiles/yelp_academic_dataset_business.json")
	end_time = time.time()
	secs = end_time - start_time
	print("Finished busn_category_pair in {} seconds, {} minutes, {} hours".format(int(secs), int(secs/60), int(secs/3600)))

	start_time = time.time()
	pairs_busn_cat = generate_similar_pairs(cat_busn_dict, 'busn_cat_pairs.csv', "business_pairs", "category_shared")
	end_time = time.time()
	secs = end_time - start_time
	print("Finished generate_similar_pairs in {} seconds, {} minutes, {} hours".format(int(secs), int(secs/60), int(secs/3600)))

	start_time = time.time()
	dict_user_pairs = similar_taste_dict_with_category("datafiles/yelp_academic_dataset_review.json")
	end_time = time.time()
	secs = end_time - start_time
	print("Finished similar_taste_dict_with_category in {} seconds, {} minutes, {} hours".format(int(secs), int(secs/60), int(secs/3600)))

	start_time = time.time()
	accuracy_with_cat_baseline(pairs_busn_cat, cat_busn_dict, dict_user_pairs)
	end_time = time.time()
	secs = end_time - start_time
	print("Finished accuracy_with_cat_baseline in {} seconds, {} minutes, {} hours".format(int(secs), int(secs/60), int(secs/3600)))
