#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:02:01 2019

@author: bartletc
@author: guzmanc
"""
import parse_arxiv_tex
#import refactor_tex_parser3
import tex_word_processing
import sys
import csv

#Returns file name from command line.
def grab_file_name():
    return sys.argv[1]
def main():
    ## Grab tex file name crom command line.
    latex_files = grab_file_name()
    
    ## Parse the tex file and return the word tokens.
    tokens = parse_arxiv_tex.latex_parser(latex_files)
    
    ## Process the tokens and write results to results folder.
    tex_word_processing.word_processing(tokens, sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
