# Algorithm to see trends in restaurant ratings.
# Vi Nguyen, Sirui Feng, Turab Hassan
# CS 123

'''
This file tries to check whether the business respond to user reviews.
Algorithm
1. Generate a dict of all business_IDs with their current rating. eg { 
	business_ID: stars}
2. For each Business, generate a history of reviews in a sorted order. eg
	{Business_ID: {date1: stars, date2:stars} etc}
3. Filter the data to business that have atleast 10 reviews. (so that we can
	see some trend.)
4. For each business start making windows of sizes starting 3 to the
	lenth of the reviews when finding fluctuations and from 3 to 10 when
	finding shifts 	
5. Find the difference between two adajacent windows, if the difference is more
	than the specified threshold, count as a shift. if the sign of the difference
	between two adajacent windows changes, count as a fluction
6. For the total Number of windows of size n, if less than 10% show fluctuation
	mark that business as converged. For shifts, if windows show a shift in
	direction of more than 75% of the time, label the trend of that restaurant
	in that direction, if it doesnt show any shift, mark it as steady, otherwise mark 
	as fluctuating. 
7. Createa a summary of at what window size more restaurants respond to users			
'''
import json
import operator
import csv
import numpy as np

business_data_filepath = '../yelp_academic_dataset_business.json'
reviews_data_filepath = '../yelp_academic_dataset_review.json'
user_data_filepath = '../yelp_academic_dataset_user.json'
test_data = 'business_testdata.csv'

#Initializing the threholds and the dict to store the results for shifts and fluctuations
shifts_thresholds = [ .5, .25]
#The idea is to capture for a window size of 3 with a thrreshold of size .25 and .5 what cases we see
shifts_cases = { 3:{.5:{},.25:{}}, 4:{.5:{},.25:{}}, 5:{.5:{},.25:{}}, 6:{.5:{},.25:{}}, 7:{.5:{},.25:{}}, 8:{.5:{},.25:{}}, 9:{.5:{},.25:{}}, 10:{.5:{},.25:{}} }

fluctuations_thresholds = [ 1, .75, .5, .25, .1]
#The idea is to capture for a threshold how many restaurants converge to a given window size
window_length_count = { 1:{},.75:{},.5:{},.25:{},.1:{} }
	


def get_reviews():
	'''
	Parse through the reviews dataset of Yelp and for each business make a dict
	like: {Business_ID: [[date1, stars], [date2,stars]] etc}. Pass this dictionary
	to count flucations and shifts 
	'''
	data = {}
	with open(reviews_data_filepath) as data_file:

		for line in data_file:	
			row = json.loads(line)
			business_id = row['business_id']
			review_id = row['review_id']
			date = row['date']
			stars = row['stars']
			user_id = row['user_id']
			item = [date, stars ]
			
			try:
				#Have already seen this ID
				data[business_id].append (item)
			except:
				#Seeing this for the first time
				data[business_id] = []
				data[business_id].append(item)
	make_windows(data)

def shifts(stars):
	'''
	Given an array of reviews(numbers from 1 to 5) for a restaurant, find the trend
	for the restaurant as outlined in the algorithm in the start. 
	'''
	for window_length in range(3,11):
				windows = [stars[i:i+window_length] for i in range(len(stars)-(window_length-1) ) ]
				windows_avg = [round(sum(y)/len(y),3) for y in windows]

				for threshold in shifts_thresholds:
					current_min = windows_avg[0] - threshold
					current_max = windows_avg[0] + threshold
					check = { 'up': 0, 'down':0 }
					for i in range(1,len(windows_avg)):
						running_avg = windows_avg[i]

						if running_avg > current_max:
							check['up'] = check.get('up',0) + 1
							current_max = running_avg + threshold
							current_min = running_avg - threshold
						if running_avg < current_min:
							check['down'] = check.get('down', 0) + 1
							current_max = running_avg + threshold
							current_min = running_avg - threshold	
					
					up = check['up']
					down = check['down']
					total = len(windows_avg)
					if up > 0 and down > 0:
						if up/(up + down) >.75:
							shifts_cases[window_length][threshold][2] = shifts_cases[window_length][threshold].get(2,0) + 1
						elif   down/(up + down) > .75:
							shifts_cases[window_length][threshold][3] = shifts_cases[window_length][threshold].get(3,0) + 1
						else:
							shifts_cases[window_length][threshold][4] = shifts_cases[window_length][threshold].get(4,0) + 1
					if down > 0 and up ==0:
							shifts_cases[window_length][threshold][3] = shifts_cases[window_length][threshold].get(3,0) + 1
					if down==0 and up > 0:
							shifts_cases[window_length][threshold][2] = shifts_cases[window_length][threshold].get(2,0) + 1
					if up == 0 and down == 0:
							shifts_cases[window_length][threshold][1] = shifts_cases[window_length][threshold].get(1,0) + 1

def fluctuations(stars, reviews):
	'''
	Given an array of reviews(numbers from 1 to 5) for a restaurant, 
	find the fluctuations for the restaurant as outlined in the algorithm 
	in the start.
	'''
	for x in fluctuations_thresholds:
				
				for window_length in range(3,len(reviews)):

					windows = [stars[i:i+window_length] for i in range(len(stars)-(window_length-1) ) ]
					windows_avg = [round(sum(y)/len(y),3) for y in windows]
					difference_in_difference = []
					for i in range(len(windows_avg)-1):
						if -x <= windows_avg[i+1] - windows_avg[i] <= x:

							difference_in_difference.append(0)
						elif windows_avg[i+1] - windows_avg[i] >= x:
							
							difference_in_difference.append(1)
						else:
							
							difference_in_difference.append(-1)
					
					fluctuations_flags = [value for value in difference_in_difference if value != 0]
					
					fluctuations = list(map( lambda i,j:i*j, fluctuations_flags[1:], fluctuations_flags[:-1]) )
					
					fluctuations_count = fluctuations.count(-1)
					
					fluctuation_percentage = round(fluctuations_count/len(windows), 2)
					
					if window_length == len(reviews):
						#means that we the restaurant has too much fluctuation
						window_length_count[x][window_length] = window_length_count[x].get(window_length, 0) + 1
						break
					if fluctuation_percentage <= .10:
						#Means we have converged
						window_length_count[x][window_length] = window_length_count[x].get(window_length, 0) + 1
						break

def make_windows (data_dict):
	'''
	Using the dict of the type { busines ID:[reviews] }make windows of
	size 3 to 10. Using the windows  
	'''
	print('starting windows')
	rv = {}
	counter = 0
	#For each business sorting by date first and then making windows.
	
	for business_id in data_dict.keys():
		counter += 1
		print(counter)
		data_dict[business_id].sort(key = operator.itemgetter(0))
		reviews = data_dict[business_id]
	#Once we have sorted the stars and by date, remove the date and get only the stars
		stars = [stars_only[1] for stars_only in reviews]
	#Looking only at Business with more than 10 reviews 
		if len(reviews) >= 10:
			shifts(stars)
			fluctuations(stars, reviews) 
	
	#output the results	
	writer = csv.writer (open('shifts.csv', 'w', newline = '') )
	for key, value in shifts_cases.items():
		writer.writerow([key, value])
	
	print(window_length_count)
	writer = csv.writer (open('fluctuations.csv', 'w', newline = '') )
	for key, value in window_length_count.items():
		writer.writerow([key, value])


get_reviews()


