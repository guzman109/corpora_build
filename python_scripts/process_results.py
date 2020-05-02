"""
Created on Fri May 1 2020

@author: guzmanc
"""
import sys
import glob
import pandas as pd
from numpy import zeros

## Reads every n-gram of the text file and adds them to the dictionary and keeps track of the occurence of each word for this 
## arXiv folder.
def read_and_count(path, dictionary):
	try:
		with open(path) as f:
			words = f.read().splitlines()
		for word in words:
			if word in dictionary:
				dictionary[word] += 1
			else:
				dictionary[word] = 1
	except IOError as e:
		print('Operation failed: %s:' % e.strerror)
	return dictionary

## Creates the dataframe to be able to extract it to a csv file. Max rows is the length of the biggest 
##  list between (c1,c2,c3,q1,q2,q3,qc1,qc2,qc3). This is needed to be able to make a matrix that pd.DataFrame can use.
def create_df(lists, df, max_rows):
	for l in lists:
		n = max_rows - len(l)
		words = list(l.keys())
		values = list(l.values())
		words.extend(['']*n)
		values.extend(['']*n)
		df.append(words)
		df.append(values)
	return df
## Calls create_df to make the dataframe (df). Uses the transpose (df.T) to make the csv file.
def create_csv(qc_lists, q_lists, c_lists, max_rows):
	data = []
	for l in [qc_lists, q_lists, c_lists]:
		data = create_df(l, data, max_rows)
	df = pd.DataFrame(data).T
	
	# Column names
	df.columns = ['qc1', 'count', 'qc2', 'count', 'qc3', 'count', 'q1', 'count', 'q2', 'count', 'q3', 'count', 'c1', 'count', 'c2', 'count', 'c3', 'count']

	# Cretae csv and write elements from df.
	df.to_csv(sys.argv[1]+'final_results.csv')

def main():
	# Path to results folder for this arxiv.
	path_to_results = '/home/gdbartlettclab/cxg078/Documents/corpora_build/results/' + sys.argv[1]
	
	# Paths to lists with arxiv results.
	qc1_files = glob.glob(path_to_results + '/QC_lists/QC1_lists/*.txt')
	qc2_files = glob.glob(path_to_results + '/QC_lists/QC2_lists/*.txt')
	qc3_files = glob.glob(path_to_results + '/QC_lists/QC3_lists/*.txt')
	
	q1_files = glob.glob(path_to_results + '/Q_lists/Q1_lists/*.txt')
	q2_files = glob.glob(path_to_results + '/Q_lists/Q2_lists/*.txt')
	q3_files = glob.glob(path_to_results + '/Q_lists/Q3_lists/*.txt')
	
	c1_files = glob.glob(path_to_results + '/C_lists/C1_lists/*.txt')
	c2_files = glob.glob(path_to_results + '/C_lists/C2_lists/*.txt')
	c3_files = glob.glob(path_to_results + '/C_lists/C3_lists/*.txt')
	
	# Initialize dictionaries for each list.
	qc1, qc2, qc3 = dict(), dict(), dict()
	q1, q2, q3 = dict(), dict(), dict()
	c1, c2, c3 = dict(), dict(), dict()
	
	# Read lists and count the occurrence of  the words between files.
	## QC lists
	for path in qc1_files:
		qc1 = read_and_count(path, qc1)
	for path in qc2_files:
		qc2 = read_and_count(path, qc2)
	for path in qc3_files:
		qc3 = read_and_count(path, qc3)
	
	## Q lists
	for path in q1_files:
		q1 = read_and_count(path, q1)
	for path in q2_files:
		q2 = read_and_count(path, q2)
	for path in q3_files:
		q3 = read_and_count(path, q3)
	
	## C lists
	for path in c1_files:
		c1 = read_and_count(path, c1)
	for path in c2_files:
		c2 = read_and_count(path, c2)
	for path in c3_files:
		c3 = read_and_count(path, c3)
	

	# Sort the words with highest count first.
	## QC lists
	qc1 = dict(sorted(qc1.items(), key=lambda x:x[1], reverse=True))
	qc2 = dict(sorted(qc2.items(), key=lambda x:x[1], reverse=True))
	qc3 = dict(sorted(qc3.items(), key=lambda x:x[1], reverse=True))
	
	## Q lists
	q1 = dict(sorted(q1.items(), key=lambda x:x[1], reverse=True))
	q2 = dict(sorted(q2.items(), key=lambda x:x[1], reverse=True))
	q3 = dict(sorted(q3.items(), key=lambda x:x[1], reverse=True))

	## C lists
	c1 = dict(sorted(c1.items(), key=lambda x:x[1], reverse=True))
	c2 = dict(sorted(c2.items(), key=lambda x:x[1], reverse=True))
	c3 = dict(sorted(c3.items(), key=lambda x:x[1], reverse=True))
	
	# Used to make the dataframe where the number of rows have to be the same for ever column.
	max_rows = max([len(qc1),len(qc2),len(qc3),len(q1),len(q2),len(q3),len(c1),len(c2),len(c3)])
	create_csv((qc1,qc2,qc3),(q1,q2,q3),(c1,c2,c3), max_rows)
if __name__ == '__main__':
	main()
