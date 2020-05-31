import sys
import os
import numpy as np

## Read the file and separate the string and the corresponding probability. 
def read_list(path):
	corpus = dict()
	with open(os.path.join(path, 'lists_with_freq/no_cutoff', sys.argv[1]), "r") as f:
		while True:
			line = f.readline()
			if line:
				line = line.rstrip().split('\t')
				corpus[line[0]] = np.float(line[1])
			else:
				break
	return corpus

## Write results to file. Cut off is the expected value from the probability distribution.
def write_list_with_cutoff(corpus, path):
	with open(os.path.join(path, 'lists_with_freq/mean_cutoff_%s'%sys.argv[1]), "w") as f:
		cutoff = np.mean(np.array(list(corpus.values())))# + np.std(np.array(list(corpus.values())))
		for word in corpus:
			if corpus[word] >= cutoff:
				f.write(f'{word:<50}\t{corpus[word]:>.8f}\n')
	with open('mean_%s'%sys.argv[1], "w") as f:
		f.write(str(cutoff))
	

def main():
	path = '/home/gdbartlettclab/cxg078/Documents/corpora_build/results_third_run'
	corpus = read_list(path)
	write_list_with_cutoff(corpus,path)

if __name__ == '__main__':
    main()
