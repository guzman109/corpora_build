##!/usr/bin/env python
## coding: utf-8


"""
Created on Fri May 1 2020

@author: guzmanc
"""
import sys
import re
from glob import glob
import numpy as np

#### Reads every n-gram of the text file and adds them to the dictionary and keeps track of the occurence of each word for this 
#### arXiv folder.
def read_and_count(path, dictionary):
    with open(path) as f:
        words = f.read().splitlines()
    temp = set(words)
    for word in words:
##             if not re.search('[^a-z\s]', word):
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary

#### Calls create_df to make the dataframe (df). Uses the transpose (df.T) to make the csv file.
def create_txt_file(corpus, noise, path, list_num):
    print('Writing %s List'%list_num)

    total = sum(list(corpus.values()))
    ## Write corpus to files
    with open(path+'%s.txt'%list_num, "w") as f_out:
        for word in corpus:
            f_out.write(f'{word:<20}\t{np.divide(corpus[word],total):>.8f}'+'\n')

def make_corpus(list_type, list_num):
    ## Path to results folder for this arxiv.
    path_to_results = '/home/gdbartlettclab/cxg078/Documents/corpora_build/results_second_run/nodes/' ##/node%s'%(sys.argv[1])

    ## Paths to lists with arxiv results.
    list_files = glob(path_to_results + 'node[1-5]/*/%s_lists/%s_lists/%s_[0-9]*.txt'
                      %(list_type.upper(), list_type.upper() + list_num, list_type + list_num))
    with open(path_to_results + 'total_%s_files.txt'%(list_type.upper()+list_num), "w") as f:
        f.write(str(len(list_files)))
    ## Initialize dictionaries for each list.
    corpus = dict()
    
    ## Read lists and count the occurrence of  the words between files.
    print('Reading %s%s  Lists'%(list_type, list_num))
    for path in list_files:
        corpus = read_and_count(path, corpus)
    
    corpus = dict(sorted(corpus.items(), key=lambda x:x[1], reverse=True))
    noise = []
    create_txt_file(corpus, noise, path_to_results, list_type.upper() + list_num)

make_corpus(sys.argv[1], sys.argv[2])
