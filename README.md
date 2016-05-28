# YelpInsighters: Project Notes

##Notes from class re: Project (5/25)
* Submit all code, scripts, anything you worked on
* Don’t upload any datafiles from git (expect Matthew to access the files as we did (via S3)

### Writeup (Casual)
* Data
* Hypotheses
* Algorithms
* Big data approaches
* Talk about the scale of what you did and how “big” it was
* What you learned, what challenged you
* Results

### Presentation
* Present what we’ve done thus far (okay if there are things we’re working on)
* Don’t share stuff that we won’t get done (i.e. don't set Matthew’s expectations high)


Question for Matthew (May 18):
Window:
Which size of window would be the most appropriate?(3-10) For larger size of window, the probability of seeing a  change is smaller, we see a more sustained shift. → window large enough to keep things smooth instead of up-and-down fluctuations
At which level do we want to do the final analysis output, window size? Or business level?
Come up with 1-size for window
3 is a clear minimum
100 is probably too big
Probably won’t go above 10
Swings
Possible that restaurants dip back and forth
Improves and stays
Improves and stays and improves and stays
Consider duration of changes/quality-levels

Similar users having similar tastes:
We define similar users as those who have gone to at least two same business, and we further define similar tastes as given the two users rate two restaurants similar (within a threshold of 0.5), they rate the third restaurant similarly.
Final Output: ?
Feedback re: list with iter.combination & mrjob: don’t create list unless you need/want to keep EVERYTHING in memory


Feedback from Matthew:
EC2-xlarge (aws); otherwise, use MR
AWS-mr-S3
Storing files: EBS, S3(preferred for MRjob)

Questions for Matthew:
Strategically better way to scan through less times of json file
Where to split MRjob
Writing to CSV is running into memory issues --should we try a different output filetype?
Updates on where we are
Good sense of how we can answer: Do similar users like similar restaurants?
Starting to think of next question: Do we see shifts in performance/user satisfaction via Yelp (i.e. do businesses react to reviews? And do users care?)

5/7
TO DOS:

1. Generate user pairs who have gone to the same restaurant (Sirui):
Assume the following data format
similar_users = {(user1_id,user2_id):{ 'cnt_same_busn_review': 3, 
business1_id: (star_ratings_user1, star_ratings_user2), 
business2_id: (star_ratings_user1, star_ratings_user2), 
business3_id: (star_ratings_user1, star_ratings_user2)}}

2. Create clusters of restaurant categories, and pairs of restaurants based on similar categorization
to potentially use as a feature to test whether users are similar (Vi)

3A. Test whether (Vi):
	A. users who gave the same rating for one restaurant will give the same ratings for another restaurant
		A1. Does it matter if the restaurant shares a similar categorization?
	B. users who gave ratings within 0.5 stars of one restaurant, will give the same ratings within 0.5 stars for another restaurant
		B1. Does it matter if the restaurant shares a similar categorization?
	C. users who gave ratings within 1 star of one restaurant, will give the same rating within 1 star for another restaurant
		C1. Does it matter if the restaurant shares a similar categorization?

3B. Test whether:
	A. users who gave the same rating for two restaurants will give the same ratings for another restaurant
		A1. Does it matter if the restaurants share a similar categorization?
	B. users who gave ratings within 0.5 stars of two restaurants, will give the same ratings within 0.5 stars for another restaurant
		B1. Does it matter if the restaurants share a similar categorization?
	C. users who gave ratings within 1 star of two restaurants, will give the same rating within 1 star for another restaurant
		C1. Does it matter if the restaurants share a similar categorization?

3B. Test whether:
	A. users who gave the same rating for three restaurants will give the same ratings for another restaurant
		A1. Does it matter if the restaurants share a similar categorization?
	B. users who gave ratings within 0.5 stars of three restaurants, will give the same ratings within 0.5 stars for another restaurant
		B1. Does it matter if the restaurants share a similar categorization?
	C. users who gave ratings within 1 star of three restaurants, will give the same rating within 1 star for another restaurant
		C1. Does it matter if the restaurants share a similar categorization?

Shifts in Quality of Businesses after certain levels of performance/avg reviews:


4/30


Session with Matthew:
Windows of 9, predict the 10th = big enough
When we’re thinking about finding users similarities:
Think about clustering of restaurants (i.e. lots of Thai restaurants vs. 1 pizza)
Think of doing co-sign (?) similarities; how does the vectors compare to each other?
Promising one
Worry about finding people who are actually similar
All the questions are interesting but some may be more challenging for the data
Competition question - do we have enough data to smooth it out?
Shift in sentiment - 
Might be hard to qualify as “big data”
Project proposal guidelines
Please submit to me, by the end of the day on Monday (4/18), your project proposal. Email is fine. Please identify, in it:

- Your group: Yelp Insighters
- The data set you plan on using
-- The size of the data set, in GB
-- The number of records, lines, entries, etc. (whichever is applicable) that exist in the data set. For instance, if you have a data set of businesses, you might tell me how many businesses there are; if you have a data set of comments to blog posts, you might tell me how many comments in total there are. This is to give me a sense of how many "items" are in the data set, beyond just the size in GB -- in other words, if I wanted to do a "for loop" over your data set, how many iterations would there be? An approximate answer is acceptable. If it is not possible to determine this now, please let me know.
- What kinds of hypotheses are you interested in testing with this data set? These are not commitments, but rather, to give me a sense of the things you think that might be interesting to explore and to give me a sense of the computational complexity of what you would like to achieve. I will combine this with the size of the data set to give you feedback on whether your project is sufficiently "big" data. In terms of number of hypotheses, the more the merrier here (within reason) -- I may be able to suggest which of the ideas seem the most reasonable in terms of the scale we're looking for in the project, and you may discover ones that don't pan out, so it's good to plan for attrition here.
- If you have ideas on how to write scalable algorithms, you are welcome to share, but this is not necessarily expected yet.

This is all that comes to mind now for what I need in your proposal. If I think of anything else that should also be added, I'll edit this post; please check back on Sunday night to make sure I haven't added anything in the interim. I'll try to avoid doing so, however.


April 16
Size of the dataset: Yelp dataset 2.39 GB 
Review: 2,225,213 entries (1.94GB)
Business: 77,445 entries (69MB)
Users: 552,339 (236.4MB)
Interesting questions to be asked: 
How many consecutive +/- reviews before we see a shift in sentiment (do business react?)
Does competition increase the quality of services (within a certain radius, assuming restaurants can be in multiple radius)?
Do “similar” users like similar things? /
Are “similar” users similar?
Variety of taste versus variety of food
Can we predict the next food trend?
Keyword, sentiment, key phrase




~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Proposal
·       Group members: Vi Nguyen, Sirui Feng, Turab Hassan
·       Group name: YelpInsighters
·       GitHub repository: https://github.com/siruif/yelpinsighters.git
Size of the dataset: Yelp dataset 2.39 GB
Review: 2,225,213 entries (1.94GB)
Business: 77,445 entries (69MB)
Users: 552,339 (236.4MB)
Interesting questions to be asked:
--- How many consecutive +/- reviews before we see a shift in sentiment (do business react?)		# noise?
--- Does competition increase the quality of services (within a certain radius, assuming restaurants can be in multiple radius)?	# concern about the data: noise
+++ Do “similar” users like similar things?
Are “similar” users similar?	# how to define ‘similar’? Caveat: noise. People with similar tastes can be good models for recommendation. Cosine similarity:vector of rating. 
Variety of taste versus variety of food
+++ Can we predict the next food trend?
Keyword, sentiment, key phrase		# top k streaming
Scalable algorithms:
For question 1 listed above, we plan to create windows (in terms of the number of) for comments and see if there is a shift in sentiment.
For question 2, we plan to compare each restaurant to all the other restaurants within a certain radius of range.
For question 3, we want to compare each user to users that are similar.
For question 4, we want to create windows (in terms of time) for food keywords that people mention in their comments.
