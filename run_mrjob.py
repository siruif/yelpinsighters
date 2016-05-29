# Author: Sirui Feng
# This file calls mr_upair_count_b.py and output the mr result to a csv.
# Run this file by python3 run_mrjob.py input_file(user_pair.csv)

from mr_upair_count_b import MRTotalBusiness
import sys
import csv

if __name__ == '__main__':
	with open("mr_output.csv",'w') as outfile:
		w = csv.writer(outfile, delimiter = ',')
		w.writerow(['pair', 'count'])
		job = MRTotalBusiness(args=sys.argv[1:])
		with job.make_runner() as runner:
			runner.run()
			for line in runner.stream_output():
				pair, count = job.parse_output_line(line)
				w.writerow([pair,count])