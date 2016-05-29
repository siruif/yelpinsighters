# Algorithm to identify whether similar users have similar future ratings
# Vi Nguyen, Sirui Feng, Turab Hassan

'''

TO DOS:

1. Generate user pairs who have gone to the same restaurant (Sirui):
Assume the following data format
similar_users = {user_pair: {'cnt_same_busn_review': 3, 
business_id: (star rating 1, star rating 2), business_id: (star rating 1, star rating 2),
business_id: (star rating 1, star rating 2)}}

2. Create clusters of restaurant categories, and pairs of restaurants based on similar categorization
to potentially use as a feature to test whether users are similar (Vi)

3A. Test whether (Vi):
	A. users who gave the same rating for one restaurant will give the same ratings for another restaurant
		A1. Does it matter if the restaurant shares a similar categorization?
	B. users who gave ratings within 0.5 stars of one restaurant, will give the same ratings within 0.5 stars for another restaurant
		B1. Does it matter if the restaurant shares a similar categorization?
	C. users who gave ratings within 1 star of one restaurant, will give the same rating within 1 star for another restaurant
		C1. Does it matter if the restaurant shares a similar categoriztion?

3B. Test whether:
	A. users who gave the same rating for two restaurants will give the same ratings for another restaurant
		A1. Does it matter if the restaurants share a similar categorization?
	B. users who gave ratings within 0.5 stars of two restaurants, will give the same ratings within 0.5 stars for another restaurant
		B1. Does it matter if the restaurants share a similar categorization?
	C. users who gave ratings within 1 star of two restaurants, will give the same rating within 1 star for another restaurant
		C1. Does it matter if the restaurants share a similar categoriztion?

3B. Test whether:
	A. users who gave the same rating for three restaurants will give the same ratings for another restaurant
		A1. Does it matter if the restaurants share a similar categorization?
	B. users who gave ratings within 0.5 stars of three restaurants, will give the same ratings within 0.5 stars for another restaurant
		B1. Does it matter if the restaurants share a similar categorization?
	C. users who gave ratings within 1 star of three restaurants, will give the same rating within 1 star for another restaurant
		C1. Does it matter if the restaurants share a similar categoriztion?
'''
import json
import pandas as pd 
import csv
#import time
import itertools
#from user_pair import *

#user_pairs_outfile = 'busn_cat_pairs.csv'


#from scripts.readto_pd_df import *

def read(filename, file_format, json_obj_top_level_id = None):
	'''
	inputs:
		filename = name of ifle
		file_format = type of format, currently can be 'csv' or 'json objects' 
	outputs:
		dataset in pandas dataframe format
	'''

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
			#print(key, val)
			for i in range(len(df)):
				if key in df['categories'][i]:
					#print(key, df['categories'][i])
					cat_busn_dict[key] = cat_busn_dict.setdefault(key, set())
					cat_busn_dict[key].add(df['business_id'][i])
	
	#print(cat_busn_dict)

	return cat_count_dict, df, cat_busn_dict

def generate_similar_pairs(dictname, outfilename, pairname, similarity_id):
	# business_dict records for each business, all the pairs who have gone to it
	# key is business_id, value is a list of tuples in the form of (user1,user2)
	with open(outfilename, 'w', newline = '') as outfile:
		w = csv.writer(outfile, delimiter = ',')
		w.writerow([pairname, similarity_id])

		for val in dictname:
			in_set = dictname[val]
			#itertools generates a list of tuples
			pairs = list(itertools.combinations(in_set, 2))
			for pair in pairs:
				w.writerow([pair, val])


if __name__ == '__main__':
	cat_count_dict, df, cat_busn_dict = busn_category_pair("../yelp_academic_dataset_business.json")
	generate_similar_pairs(cat_busn_dict, 'busn_cat_pairs.csv', "business_pairs", "category_shared")

