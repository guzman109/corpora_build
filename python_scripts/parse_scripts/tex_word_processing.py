import re
from nltk.corpus import stopwords
from nltk.util import ngrams
import os.path


# Begins the two main objectives of this program
def word_processing(tokens, arxiv_name, i, n):
    if (len(tokens) != 0):
        path = '/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node%s/%s/'%(n, arxiv_name)
        filtered_tokens = normalize_tokens(tokens)
        categorize_words(filtered_tokens, path, i)


# Normalizes the tokens from the tex file.
#   - Removes stop words
#   - Removes obvious non-real words (no vowels)
#   - Removes left-over non-essential symbols.
def normalize_tokens(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = []
    for token in tokens:
        if '-' == token[0]:
            continue
        if '-' == token[-1]:
            continue
        if token[0] == '\'':
            token = token[1:]
        if token.lower() not in stop_words:
            if 3 <= len(token) <= 30 and re.search('[aeiou]', token, re.I):
                filtered_tokens.append(token.lower())
    return filtered_tokens


# Categorizes the words and writes info to corresponding text files.
def categorize_words(words, path, i):
    # Create n-gram list and list to categorize the words.
    n1, n2, n3 = create_ngrams_list(words)

    # Begins categorization algorithm
    quantum_computing_count = sum('quantum comput' in s for s in n2) + sum('quantum sens' in s for s in n2) + sum(
        'quantum information' in s for s in n2)
    if n1.count('quantum') > 0:
        if quantum_computing_count > 0:
            with open(path + 'QC_lists/QC1_lists/qc1_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(n1))
            with open(path + 'QC_lists/QC2_lists/qc2_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(n2))
            with open(path + 'QC_lists/QC3_lists/qc3_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(n3))
        else:
            with open(path + 'Q_lists/Q1_lists/q1_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(n1))
            with open(path + 'Q_lists/Q2_lists/q2_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(n2))
            with open(path + 'Q_lists/Q3_lists/q3_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(n3))
    else:
        with open(path + 'C_lists/C1_lists/c1_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(n1))
        with open(path + 'C_lists/C2_lists/c2_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(n2))
        with open(path + 'C_lists/C3_lists/c3_%s.txt'%i, mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(n3))


# Creates n-gram lists and finds n-gram from the tex file.
def create_ngrams_list(tokens):
    n1_gram_list = []
    n2_gram_list = []
    n3_gram_list = []

    for ngram in list(ngrams(tokens, 1)):
        n1_gram_list.append(' '.join(ngram))
    for ngram in list(ngrams(tokens, 2)):
        n2_gram_list.append(' '.join(ngram))
    for ngram in list(ngrams(tokens, 3)):
        n3_gram_list.append(' '.join(ngram))

    return n1_gram_list, n2_gram_list, n3_gram_list
