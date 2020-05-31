import sys
import os
import numpy as np

##Read the file. Separate the string and its corresponding probability. Then add it to a dictionary.
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

## Write results to a file. Cutoff is the expected value of the prob dist + standard deviation of the prob dist.
def write_list_with_cutoff(corpus, path):
	with open(os.path.join(path, 'lists_with_freq/mean_std_cutoff/mean_std_cutoff_%s'%sys.argv[1]), "w") as f:
		cutoff = np.mean(np.array(list(corpus.values()))) + np.std(np.array(list(corpus.values())))
		for word in corpus:
			if corpus[word] >= cutoff:
				f.write(f'{word:<50}\t{corpus[word]:>.8f}\n')
	with open('mean_std_%s'%sys.argv[1], "w") as f:
		f.write(str(np.mean(np.array(list(corpus.values())))) + '\t' + str(np.std(np.array(list(corpus.values())))))
	
def main():
	path = '/home/gdbartlettclab/cxg078/Documents/corpora_build/results_third_run'
	corpus = read_list(path)
	write_list_with_cutoff(corpus,path)

if __name__ == '__main__':
    main()
