#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:02:01 2019

@author: bartletc
"""
import re
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords
import sys

fh = open(sys.argv[1])
line = fh.readline()

fh_output = open('test.clean.txt','w')

# use the read line to read further.
# If the file is not empty keep reading one line
# at a time, till the file is empty

endCondition = False

while (line and not endCondition):
    # start the conditions for when to keep a line and put in corpus versus not

    # if a line starts with a tex command
    if line.lstrip().startswith( '\\' ):
        #print('there is a line starting with backslash')
        
        # if we get to acknowledgements just stop reading the file completely
        if re.search('acknowledgement', line, re.IGNORECASE):
            # skip to the end of the tex document
            #print('end condition met')
            endCondition = True
            break
        # if we get to biblography  just stop reading the file completely
        elif re.search('reference', line, re.IGNORECASE):
            # skip to the end of the tex document
            #print('end condition met')
            endCondition = True
            break
        elif re.search('bibliography', line, re.IGNORECASE):
            # skip to the end of the tex document
            #print('end condition met')
            endCondition = True
            break
        
        # skip the sections we know we don't want, like tables and figures
        elif (re.search(r'\\begin{table',line) or re.search(r'\\begin*{table',line)):
            # skip to the end of this section
            while not re.search(r'\\end{table',line) or not re.search(r'\\end*{table',line):
                line = fh.readline()
        elif (re.search(r'\\begin{keywords',line) or re.search(r'\\begin*{keywords',line)):
            # skip to the end of this section
            while not re.search(r'\\end{keywords',line) or not re.search(r'\\end*{keywords',line):
                line = fh.readline()
        elif (re.match(r'\\begin{figure',line) or re.match(r'\\begin*{figure',line)):
            # skip to the end of this section
            #print(line)
            while (not re.match(r'\\end{figure',line) or not re.match(r'\\end*{figure',line)):
                line = fh.readline()
                #print(line)
        elif (re.search(r'\\begin{equation',line) or re.search(r'\\begin*{equation',line)):
            # skip to the end of this section
            while not re.search(r'\\end{equation',line) or not re.search(r'\\end*{equation',line):
                line = fh.readline()

        elif (re.search(r'\\begin{table',line) or re.search(r'\\begin*{table',line)):
            # skip to the end of this section
            while not re.search(r'\\end{table',line) or not re.search(r'\\end*{table',line):
                line = fh.readline()
         
        # Since we aren't skipping a section, and we aren't ending outright, 
        #   we skip what would be a single line that is a tex command
        else:
            #print('this line is just a tex command so I deleted it')
            line = fh.readline()

        # ignore comment lines, only thing left is stuff we want
    elif line.startswith( '%' ):
        #print('there is a line starting with %')
        line = fh.readline()
    else:
        ##
        ## Here are the lines that we want to process
        ## but we still have to remove inline tex commands
        ##
        # remove inline math
        line2 = re.sub('\$+(.*?)\$+','',line)
        # remove any inline tex commands (mostly citations)
        line3 = re.sub(r'\\(\w+)\{(.*?)\}','',line2)
        #print('outputting a clean line')
        fh_output.write(line3)

        line = fh.readline()

fh.close()

##
## Now we will read in the file of clean tex lines and process it with nltk
##

# process the following:
#  remve stop words
#  remove punctuation
#  remvoe EOL charaters
#  make all upper case letters into lower case let

nltk.download('stopwords')
no_stop_words = []
stop_words = set(stopwords.words('english')) 
file1 = open("test.clean.txt") 
line = file1.read()# Use this to read file content as a stream: 
file1.close()
line = line.lower()
line = re.sub(r'[^a-zA-Z0-9\s]', ' ', line)
line = re.sub(r'[^\w\s]', ' ', line)
line = re.sub(r'\_','',line)
line = re.sub(r'\n',' ',line)
line = re.sub(r'\r',' ',line)
tokens = [token for token in line.split(" ") if token != ""]

for r in tokens: 
    if not r in stop_words: 
        no_stop_words.append(''.join(r))

n1_grams = list(ngrams(no_stop_words, 1))
n2_grams = list(ngrams(no_stop_words, 2))
n3_grams = list(ngrams(no_stop_words, 3))

#for ngram in text_no_punc_no_eol:
#    n1_gram_list.append(' '.join(ngram))

n1_gram_list = []
for ngram in n1_grams:
    n1_gram_list.append(' '.join(ngram))
n2_gram_list = []
for ngram in n2_grams:
    n2_gram_list.append(' '.join(ngram))
n3_gram_list = []
for ngram in n3_grams:
    n3_gram_list.append(' '.join(ngram))


# categorize the string by keywords
#if 'quantum' in text_no_punc_no_eol:
#	if 'quantum computing' in text_no_punc_no_eol:  
#   print 'quantum only'
import os.path
if not os.path.exists("c1.txt"):
    c1=[]
    c2=[]
    c3=[]
else:
    c1 = [line.rstrip('\n') for line in open("c1.txt")]
    c2 = [line.rstrip('\n') for line in open("c2.txt")]
    c3 = [line.rstrip('\n') for line in open("c3.txt")]
    #c1.close()
    #c2.close()
    #c3.close()
    
if not os.path.exists("q1.txt"):
    q1=[]
    q2=[]
    q3=[]
else:
    q1 = [line.rstrip('\n') for line in open("q1.txt")]
    q2 = [line.rstrip('\n') for line in open("q2.txt")]
    q3 = [line.rstrip('\n') for line in open("q3.txt")]
    #q1.close()
    #q2.close()
    #q3.close()

if not os.path.exists("qc1.txt"):
    qc1=[]
    qc2=[]
    qc3=[]
else:
    qc1 = [line.rstrip('\n') for line in open("qc1.txt")]
    qc2 = [line.rstrip('\n') for line in open("qc2.txt")]
    qc3 = [line.rstrip('\n') for line in open("qc3.txt")]
    #qc1.close()
    #qc2.close()
    #qc3.close()
    
##
##  Categorize the current corpus and add unique entries to the right corpus
##
    sum('quantum comput' in s for s in n2_gram_list)
if n1_gram_list.count('quantum') > 0:
    if sum('quantum comput' in s for s in n2_gram_list) >0 or sum('quantum sens' in s for s in n2_gram_list) >0 or sum('quantum information' in s for s in n2_gram_list) >0: 
        qc1_tmp = []
        qc1_tmp = list(qc1)
        qc1.extend(x for x in n1_gram_list if x not in qc1)
        qc2_tmp = []
        qc2_tmp = list(qc2)
        qc2.extend(x for x in n2_gram_list if x not in qc2)
        qc3_tmp = []
        qc3_tmp = list(qc3)
        qc3.extend(x for x in n3_gram_list if x not in qc3)
        with open('qc1.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(qc1))
            myfile.close()
        with open('qc2.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(qc2))
            myfile.close()
        with open('qc3.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(qc3))
            myfile.close()
    else:
        q1_tmp = []
        q1_tmp = list(qc1)
        q1.extend(x for x in n1_gram_list if x not in q1)
        q2_tmp = []
        q2_tmp = list(qc2)
        q2.extend(x for x in n2_gram_list if x not in q2)
        q3_tmp = []
        q3_tmp = list(qc3)
        q3.extend(x for x in n3_gram_list if x not in q3)
        with open('q1.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(q1))
            myfile.close()
        with open('q2.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(q2))
            myfile.close()
        with open('q3.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(q3))
            myfile.close()
else:
    c1_tmp = []
    c1_tmp = list(c1)
    c1.extend(x for x in n1_gram_list if x not in c1)
    c2_tmp = []
    c2_tmp = list(c2)
    c2.extend(x for x in n2_gram_list if x not in c2)
    c3_tmp = []
    c3_tmp = list(c3)
    c3.extend(x for x in n3_gram_list if x not in c3)
    with open('c1.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(c1))
        myfile.close()
    with open('c2.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(c2))
        myfile.close()
    with open('c3.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(c3))
        myfile.close()
        
       
# function to get unique values 
# from https://www.geeksforgeeks.org/python-get-unique-values-list/
#def unique(list1): 
#      
    # insert the list to the set 
#    list_set = set(list1) 
    # convert the set to the list 
#    unique_list = (list(list_set)) 
    #for x in unique_list: 
    #    print(x) 
#    return unique_list