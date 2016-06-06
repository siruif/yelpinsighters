# Author: Sirui Feng

'''
This file counts how many same business has a pair gone to by using MR.
Performs MapReduce on user_pair.csv
Please run through run_mrjob.py
Please do not call this file directly if you want the results output to a csv.
'''

from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"\(.*?\)")

class MRTotalBusiness(MRJob):

  def mapper(self, _, line):
  	for word in WORD_RE.findall(line):
  		yield word,1
  
  def combiner(self, pair, counts):
    yield pair, sum(counts)
  
  def reducer(self, pair, counts):
  	lst = list(counts)
  	if sum(lst)>=2:
  		yield pair, sum(lst)

if __name__ == '__main__':
  MRTotalBusiness.run()