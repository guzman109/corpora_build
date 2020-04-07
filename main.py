#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:02:01 2019

@author: bartletc
"""
import refactor_parse_arxiv_tex
import tex_word_processing
import sys
import csv

#Returns file name from command line.
def grab_file_names():
    return sys.argv[1]


def main():
    latex_files = grab_file_names()
    tokens = refactor_parse_arxiv_tex.latex_parser(latex_files)
    tex_word_processing.word_processing(tokens)


if __name__ == '__main__':
    main()
