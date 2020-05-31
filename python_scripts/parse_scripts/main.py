#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:02:01 2019

@author: bartletc
@author: guzmanc
"""
import parse_arxiv_tex
import tex_word_processing
import sys

#Returns file name from command line.
def main(): 
    
    ## Parse the tex file and return the word tokens.
    tokens = parse_arxiv_tex.latex_parser(sys.argv[1])
    
    ## Process the tokens and write results to results folder.
    if tokens:
        #print(tokens)
        tex_word_processing.word_processing(tokens, sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('No Tokens')


if __name__ == '__main__':
    main()
