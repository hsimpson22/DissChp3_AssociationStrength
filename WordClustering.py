# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:52:34 2015

@author: heathersimpson

Goal of this is to cluster/group words that had a strong tendency to be remembered together and forgotten together
and see how these clusters match up with the boundaries of linguistic units (Intonation Units and clauses)
If they match up well, that is evidence that that linguistic unit is functioning to 
partition or 'chunk' spoken language in processing and/or memory representation

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.neighbors as skn

pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)

"""Read in file containing the automatically scored results 
of memory experiment. Each row in the table represents the score 
(Correct = 0 or 1)  for one word from one stimulus for one subject.
There are 101 subjs * 54 stimuli * sum of words in all stimuli = 203818 rows total """
scores = pd.read_csv('/Users/heathersimpson/Documents/Dissertation/Experiment1/Data/GS_Score_byWord_updated.csv', sep='\t')

"""Group the dataframe by stimulus, so that the scores for each word by subject 
will be easier to compare  
"""
grouped = scores.groupby('StimulusID')
#for stimulus in scores['StimulusID'].unique()
stimulus = 0 # ID for stimulus 0, ('Stimulus ID' values are integers 0-53)
stimscores = grouped.get_group(stimulus) #get_group takes label as argument, so variable stimulus should = valid StimulusID value 
stimscores['WordPosition'].max #find the max WordPosition so that it can be used to constrain the 

""" 
The dependent variable here is a binary value (Correct = no vs. Correct = yes)
Therefore we cannot use distance metrics that expect continuous variables (such as Euclidean distance)
Instead we compute Simple Matching Coeffecient (SMC) for pairs of words. 
This will create a distance matrix for all words.
The SMC is used because it weights the presence and absence of a binary attribute equally, 
and in this case we care about words being forgotten together as well as remembered together,
since my assumption is that if one being forgotten is predictive of the other being forgotten, that would be indicative of 
them having some type of unit status. 
 I will try this for all pairs with each other
"""

"""Replace "no" and "yes" with 0 and 1 in Correct column
"""
WP = stimscores.groupby('WordPosition')
WP.get_group(71)
WP.get_group(70)
#then do zip on correct values and see if sum = 0 or 2

"""use kneighbors on WordPosition to create connectivity graph"""
connectivity_matrix = skn.kneighbors_graph(stimscores['WordPosition'].values)

"""Calculate the clusters with one iteration, and then recompute the 
connectivity matrix with k-neighbors set to 2. Repeat."""
