#!/usr/bin/env python
# coding: utf-8

##Update nltk words
import nltk
nltk.download('words')

from nltk.corpus import words
import numpy as np
import re
import sys

##Detects random string by training a model to know all possible n_gram of characters from each word in nltk.words corpus.
def filter_trigram(corpus, train_corpus, f_name):

    ## Detect random string model. Uses Markov Chain approach where if the previous n_gram exists 
    ## then the you can continue with it being an actual word. The data structure is a dicitionary where
    ## trigram_markov_chain_model{str: list['str']}. FOR EXAMPLE: 'the' {'t': 'he'}
    ## Trained on nltk.words
    trigram_markov_chain_model = dict()
    
    for word in train_corpus:
        if len(word) >= 3 and (not re.search(r'[^a-z]', word)):
            for i in range(len(word)-2):
                if word[i] in trigram_markov_chain_model:
                    s = '%s%s'%(word[i+1],word[i+2])
                    trigram_markov_chain_model[word[i]].add(s)
                else:
                    trigram_markov_chain_model[word[i]] = set()
                    
                    s = '%s%s'%(word[i+1],word[i+2])
                    trigram_markov_chain_model[word[i]].add(s)

    ##Used to separate words from not words
    not_noise = dict()

    ##Files to write results
    f_out1 = open('/home/gdbartlettclab/cxg078/Documents/corpora_build/results_third_run/filter_rand/%s_3gram_words_%s_cutoff.txt'%(f_name, sys.argv[2]), "w")
    f_out2 = open('/home/gdbartlettclab/cxg078/Documents/corpora_build/results_third_run/filter_rand/%s_3gram_noise.txt'%(f_name), "w")
    f_out3 = open('/home/gdbartlettclab/cxg078/Documents/corpora_build/results_third_run/filter_rand/%s_3gram_below_%s_cutoff.txt'%(f_name, sys.argv[2]), "w")

    ## Begins by looking at each n_gram token (1,2,or 3) from the corpus, then it looks at each individual substring (t) in the n_gram token (1, 2, or 3). 
    ## Next it looks at each present character (c) in t. Followed by looking ahead at the next two characters (n_char) in t. 
    ## If c is a key in the model (trigram_markov_chain_model) and n_char is in model[c] (trigram_markov_chain_model[c]=list['str']), then t is a real word.
    ## If for all t in token, then token is a real string of word(s).
    for token in corpus:
        is_word = True
        for t in token.split():
            for c in range(len(t)-2):
                    n_char = '%s%s'%(t[c+1],t[c+2])
                    if t[c] not in trigram_markov_chain_model:
                        is_word = False
                        break
                    if n_char not in trigram_markov_chain_model[t[c]]:
                        is_word = False
                        break
        if is_word:
            not_noise[token] = corpus[token]
        else:
            f_out2.write(f'{token:<50}{corpus[token]:>.8f}\n')

    ## Used to filter further by either the mean or mean + std.
    if sys.argv[2] == 'mean':
        threshold = np.mean(list(not_noise.values()))
    elif sys.argv[2] == 'mean_std':
        threshold = np.add(np.mean(list(not_noise.values())), np.std(list(not_noise.values())))
    else:
        threshold = 0

    ## Write results to file.
    for word in not_noise:
        if not_noise[word] >= threshold:
            f_out1.write(f'{word:<50}{not_noise[word]:>.8f}\n')
        else:
            f_out3.write(f'{word:<50}{not_noise[word]:>.8f}\n')
    f_out1.close()
    f_out2.close()
    f_out3.close()

    with open('%s_3gram_words_mean_std.txt'%f_name, "w") as f:
        f.write('mean:\t')
        f.write(str(np.mean(list(not_noise.values())))+'\n')
        f.write('std:\t')
        f.write(str(np.std(list(not_noise.values())))+'\n')

def main():
    ##Set up markov_chain_model
    train_corpus = [w.lower() for w in words.words('en') if not re.search(r'[^a-zA-Z]', w)]
    train_corpus = set(train_corpus)

    ## Name of file to read.
    f_name = sys.argv[1]

    ##Read file and split words and probabilities.
    corpus = dict()
    with open('/home/gdbartlettclab/cxg078/Documents/corpora_build/results_third_run/lists_with_freq/n/%s.txt'%(f_name), "r") as f:
            while True:
                line = f.readline()
                if line:
                    line = line.strip().split('\t')
                    corpus[line[0].strip()] = np.float(line[1])
                else:
                    break

    filter_trigram(corpus, train_corpus, f_name)

if __name__=='__main__':
    main()

