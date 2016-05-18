import json
reviews_data_filepath = '../yelp_academic_dataset_review.json'


with open(reviews_data_filepath) as data_file, open('reviews_testdata.json', 'w') as test_data_file:
	for line in data_file:
		row = json.loads(line)
		business_id = row['business_id']
		if business_id == "1qCuOcks5HRv67OHovAVpg":
			print("found one")
			test_data_file.write(line)



#{"votes": {"funny": 0, "useful": 0, "cool": 0}, "user_id": "PUFPaY9KxDAcGqfsorJp3Q", "review_id": "Ya85v4eqdd6k9Od8HbQjyA", "stars": 4, "date": "2012-08-01", "text": "Mr Hoagie is an institution. Walking in, it does seem like a throwback to 30 years ago, old fashioned menu board, booths out of the 70s, and a large selection of food. Their speciality is the Italian Hoagie, and it is voted the best in the area year after year. I usually order the burger, while the patties are obviously cooked from frozen, all of the other ingredients are very fresh. Overall, its a good alternative to Subway, which is down the road.", "type": "review", "business_id": "5UmKMjUEUNdYWqANhGckJw"}
