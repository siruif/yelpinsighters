import json
import csv
reviews_data_filepath = '../yelp_academic_dataset_reviews.json'
business_data_filepath = '../yelp_academic_dataset_business.json'

def reviews_for_specific_business():
	with open(reviews_data_filepath) as data_file, open('business_testdata.csv', 'w') as test_data_file:
		for line in data_file:
			row = json.loads(line)
			business_id = row['business_id']
			if business_id == "1qCuOcks5HRv67OHovAVpg" or business_id == "tv8cS4aaA1VDaInYgggb6g":
				print("found one")
				test_data_file.write(line)

def reviews_count_tocsv():
	'''
	dict_keys(['categories', 'open', 'full_address', 'type', 'latitude', 'stars', 
	'review_count', 'longitude', 'name', 'attributes', 'neighborhoods', 'city', 'business_id', 'hours', 'state'])
	'''
	with open(business_data_filepath,encoding="utf8") as data_file, open('business_data.csv', 'w', encoding='utf-8' ) as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',' , lineterminator='\n')

		spamwriter.writerow(['business_id', 'business_name', 'review_count', 'latitude','longitude','n_hood'])
		for line in data_file:
			
			row = json.loads(line)
			business_id = row['business_id']
			business_name = row['name']
			review_count = row['review_count']
			latitude = row['latitude']
			longitude = row['longitude']
			n_hood = row['neighborhoods']
			state = row['state']
			row_to_write = [business_id, business_name, review_count, latitude,longitude,n_hood, state]
			#print(row_to_write)
			spamwriter.writerow(row_to_write)

reviews_count_tocsv()
#{"votes": {"funny": 0, "useful": 0, "cool": 0}, "user_id": "PUFPaY9KxDAcGqfsorJp3Q", "review_id": "Ya85v4eqdd6k9Od8HbQjyA", "stars": 4, "date": "2012-08-01", "text": "Mr Hoagie is an institution. Walking in, it does seem like a throwback to 30 years ago, old fashioned menu board, booths out of the 70s, and a large selection of food. Their speciality is the Italian Hoagie, and it is voted the best in the area year after year. I usually order the burger, while the patties are obviously cooked from frozen, all of the other ingredients are very fresh. Overall, its a good alternative to Subway, which is down the road.", "type": "review", "business_id": "5UmKMjUEUNdYWqANhGckJw"}
