# Algorithm to identify business pairs who share the same categories
# Vi Nguyen, Sirui Feng, Turab Hassan

import json
import pandas as pd 
import csv
import time
import itertools


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
	with open(outfilename, 'w', newline = '') as outfile:
		w = csv.writer(outfile, delimiter = ',')
		w.writerow([pairname, similarity_id])

		for val in dictname:
			in_set = sorted(dictname[val])
			#itertools generates a list of tuples
			for pair in itertools.combinations(in_set, 2):
				w.writerow([pair, val])


if __name__ == '__main__':
	print("initializing...")
	start_time = time.time()
	cat_count_dict, df, cat_busn_dict = busn_category_pair("datafiles/yelp_academic_dataset_business.json")
	end_time = time.time()
	secs = end_time - start_time
	print("Finished busn_category_pair in {} seconds, {} minutes, {} hours".format(int(secs), int(secs/60), int(secs/3600)))

	start_time = time.time()
	generate_similar_pairs(cat_busn_dict, 'busn_cat_pairs.csv', "business_pairs", "category_shared")
	end_time = time.time()
	secs = end_time - start_time
	print("Finished generate_similar_pairs in {} seconds, {} minutes, {} hours".format(int(secs), int(secs/60), int(secs/3600)))
