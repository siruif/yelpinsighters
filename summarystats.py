import json


def business_data():
	'''
	Parse throught the business dataset of Yelp and find the summary statistics.
	Each row is dictionary with the following Keys (['categories', 'open', 'full_address', 
	'type', 'latitude', 'stars', 'review_count', 'longitude', 'name', 'attributes', 'neighborhoods',
	'city', 'business_id', 'hours', 'state']) 
	'''
	
	with open('yelp_academic_dataset_business.json') as data_file:    
		count_of_business = 0
		count_of_business_chicago = 0
		type_of_business = set()
		cities_represented = set()
		cities = set()
		for line in data_file:
			row = json.loads(line)
			
			row_type_of_categories = row['categories']
			for category in row_type_of_categories:
				type_of_business.add(category)
			
			city = row['city']
			#print(city)
			cities_represented.add(city)
			if city == '':
				count_of_business_chicago += 1
			count_of_business += 1
		
		list_of_categories = list(type_of_business)
		list_of_categories.sort()
		
		list_of_cities = list(cities_represented)
		list_of_cities.sort()

		print( 'count_of_business',count_of_business )
		print( 'count_of_business_chicago', count_of_business_chicago )
		print( 'cities_represented', len(list_of_cities), list_of_cities )
		print( 'list_of_categoreis',len(list_of_categories),list_of_categories )

def user_data():
	'''
	Parse throught the user dataset of Yelp and find the summary statistics. Each row is dictionary 
	with the following keys:
	(['average_stars', 'elite', 'compliments', 'type', 'yelping_since', 'fans', 
	'review_count', 'name', 'user_id', 'friends', 'votes']
	'''
	with open('yelp_academic_dataset_user.json') as data_file:

		user_count = 0
		for line in data_file:
			row = json.loads(line)
			user_count += 1
		
		print( 'user_count',user_count )  


def reviews_data():
	'''
	Parse throught the user dataset of Yelp and find the summary statistics. Each row is dictionary 
	with the following keys:
	(['text', 'date', 'review_id', 'stars', 'business_id', 'votes', 'user_id', 'type'])
	'''
	with open('yelp_academic_dataset_review.json') as data_file:

		reviews = 0
		users   = set()
		business = set()
		for line in data_file:
			row = json.loads(line)
			users.add(row['user_id'])
			business.add(row['business_id'])
			reviews += 1

		print('No Users who reviewed', len(users))
		print('No of Business who got reviewd', len(business))
		print('No of reviews', reviews)	

			
