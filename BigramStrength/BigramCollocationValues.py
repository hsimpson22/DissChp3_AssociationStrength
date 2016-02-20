# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:03:22 2015

@author: heathersimpson

We are going to extract measures of collocation strength for the bigrams in the Experiment 1 stimuli


Step 1. Extract Bigrams from  
Step 2. Bigram lookup table  
"""


import os
import numpy as np
import pandas as pd
from nltk.tree import Tree
from nltk import FreqDist
from nltk.grammar import is_terminal,Production,induce_pcfg,Nonterminal
from nltk.collocations import BigramCollocationFinder

ClauseInfo = pd.read_csv('ClauseBoundaryInfo.csv', sep='\t', index_col=0)


#Extract all the words from parsed SBC corpus files
PARSEDdir = "/Users/heathersimpson/Documents/Dissertation/Articles/Chp4_SynPrimingIUs/PARSED/"

files = [f for f in listdir(PARSEDdir) if re.match(r".*parsed$",f)]
