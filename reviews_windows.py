'''
This file tries to check whether the business respond to user reviews.
Algorithm
1. Generate a dict of all business_IDs with their current rating. eg { 
business_ID: stars}
2. For each Business, generate a history of reviews in a sorted order. eg
{Business_ID: {date1: stars, date2:stars} etc}
3. Filter the data to business that have atleast 10 reviews.
4. For each business start making windows of sizes starting 3 to 10.
5. Compare two adjacent windows and define business_response = 1, if the avg 
   rating of the two windows differ by 1.
6. For the total Number of windows of size n, if the majority of windows show 
   a business response record that.
7. Createa a summary of at what window size more restaurants respond to users			
'''
import json
import operator

business_data_filepath = '../yelp_academic_dataset_business.json'
reviews_data_filepath = '../yelp_academic_dataset_review.json'

def business_data():
	'''
	Parse through the business dataset of Yelp and return the business names.
	Each row is dictionary with the following Keys (['categories', 'open', 
	'full_address', 'type', 'latitude', 'stars', 'review_count', 'longitude',
	'name', 'attributes', 'neighborhoods','city', 'business_id', 'hours', 'state']) 
	'''
	with open(business_data_filepath) as data_file:    
		business_id = set()
		for line in data_file:
			row = json.loads(line)
			business_id.add( row['business_id'] )
	return business_id

def get_reviews():
	'''
	Parse through the reviews dataset of Yelp and for each business make a dict
	like: {Business_ID: {date1: stars, date2:stars} etc}
	(['text', 'date', 'review_id', 'stars', 'business_id', 'votes', 'user_id', 'type']) 
	'''

	data = {}
	print('starting')
	#Making the data dictionary
	with open("reviews_testdata.json") as data_file:

		for line in data_file:
			row = json.loads(line)
			business_id = row['business_id']
			review_id = row['review_id']
			date = row['date']
			stars = row['stars']
			item = [date, stars]
			try:
				data[business_id].append (item)
			except:
				data[business_id] = []
				data[business_id].append (item)
	#For each business sorting by date first and then making windows.
	for key in data.keys():
		data[key].sort(key = operator.itemgetter(0))
		reviews = data[key]
	#Once we have sorted the stars and by date, remove the data and get only the stars
		stars = [stars_only[1] for stars_only in reviews]
	#Looking only at Business with more than 10 reviews 
		if len(reviews) >= 10:
	#Making windows of size 3, 4 and 5. Can change this later
			for window_length in range(3,6):
				print("window length", window_length)
				windows = [stars[i:i+window_length] for i in range(len(stars)-(window_length-1) ) ]
				print (windows) 					




	#return data

get_reviews()


