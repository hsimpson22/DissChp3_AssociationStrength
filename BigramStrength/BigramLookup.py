# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 13:33:20 2016

@author: heathersimpson

Script to look up pointwise mutual information values for bigrams in the Santa Barbara Corpus, for the bigrams in my stimuli, contained in WordPairsScores.csv
"""
import pandas as pd
from nltk import WordNetLemmatizer
#==============================================================================
# Opening the SBC Bigrams and WordPairs files
#==============================================================================

WordPairs = pd.read_csv("../WordPairsScores.csv", sep="\t", index_col=0)

SBC_bigrams = pd.read_csv("SBC-bigrams.txt", sep="\t")


WordPairs.columns
SBC_bigrams.columns

SBC_bigrams['Word1'] SBC_bigrams['Word2']

wnl = WordNetLemmatizer()