import re
from nltk.corpus import stopwords
from nltk.util import ngrams
import os.path

# Begins the two main objectives of this program
def word_processing(tokens):
    filtered_tokens = normalize_tokens(tokens)
    categorize_words(filtered_tokens)

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
def categorize_words(words):
    # Create n-gram list and list to categorize the words.
    n1, n2, n3 = create_ngrams_list(words)
    c1, c2, c3 = create_non_quantum_lists()
    q1, q2, q3 = create_quantum_list()
    qc1, qc2, qc3 = create_quantum_computing_list()

    # Begins categorization algorithm
    quantum_computing_count = sum('quantum comput' in s for s in n2) + sum('quantum sens' in s for s in n2) + sum(
        'quantum information' in s for s in n2)
    if n1.count('quantum') > 0:
        if quantum_computing_count > 0:
            qc1.extend(x for x in n1 if x not in qc1)
            qc2.extend(x for x in n2 if x not in qc2)
            qc3.extend(x for x in n3 if x not in qc3)
            with open('qc1.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(qc1))
            with open('qc2.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(qc2))
            with open('qc3.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(qc3))
        else:
            q1.extend(x for x in n1 if x not in q1)
            q2.extend(x for x in n2 if x not in q2)
            q3.extend(x for x in n3 if x not in q3)
            with open('q1.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(q1))
            with open('q2.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(q2))
            with open('q3.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(q3))
    else:
        c1.extend(x for x in n1 if x not in c1)
        c2.extend(x for x in n2 if x not in c2)
        c3.extend(x for x in n3 if x not in c3)
        with open('c1.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(c1))
        with open('c2.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(c2))
        with open('c3.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(c3))

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

# Creates lists for tex files that do not contain quantum info.
def create_non_quantum_lists():
    c1 = []
    c2 = []
    c3 = []
    if os.path.exists('c1.txt'):
        try:
            with open('c1.txt') as f1, open('c2.txt') as f2, open('c3.txt') as f3:
                c1 = [line.rstrip('\n') for line in f1]
                c2 = [line.rstrip('\n') for line in f2]
                c3 = [line.rstrip('\n') for line in f3]
        except IOError as e:
            print('Operation failed: %s' % e.strerror)
    return c1, c2, c3

# Creates lists for tex files that contain quantum info but not quantum computing.
def create_quantum_list():
    q1 = []
    q2 = []
    q3 = []
    if os.path.exists('q1.txt'):
        try:
            with open('q1.txt') as f1, open('q2.txt') as f2, open('q3.txt') as f3:
                q1 = [line.rstrip('\n') for line in f1]
                q2 = [line.rstrip('\n') for line in f2]
                q3 = [line.rstrip('\n') for line in f3]
        except IOError as e:
            print('Operation failed: %s' % e.strerror)
    return q1, q2, q3

# Creates lists for tex fiels that contain quantum computing info only.
def create_quantum_computing_list():
    qc1 = []
    qc2 = []
    qc3 = []
    if os.path.exists('qc1.txt'):
        try:
            with open('qc1.txt') as f1, open('qc2.txt') as f2, open('qc3.txt') as f3:
                qc1 = [line.rstrip('\n') for line in f1]
                qc2 = [line.rstrip('\n') for line in f2]
                qc3 = [line.rstrip('\n') for line in f3]
        except IOError as e:
            print('Operation failed: %s' % e.strerror)
    return qc1, qc2, qc3
