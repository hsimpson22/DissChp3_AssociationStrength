# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:37:37 2015

@author: heathersimpson
"""

"""
This script will analyze a dataset from a memory experiment performed by the author

The purpose of the experiment was to analyze the effects of intonation (e.g. pitch changes) 
in natural spoken language on working memory. Specifically, we
investigated the hypothesis that intonation may be used to 'chunk' speech into easy-to-process units, 
Subjects listened to a series of short clips of naturally-produced spoken American English, and were asked to type everything
they heard, from memory, immediately following each clip. 

The clips were of various lengths in clauses, words, and intonation units (a type of intonational phrase)

The current analysis is investigating the hypothesis that if intonation units are equivalent to 'chunks' in working memory 
during processing of speech, that there should be some measurable degree of 
association added between words in IUs. Therefore, words within IU boundaries should be more likely
to be either remembered together or forgotten together, and words across boundaries would be less likely to 
match in their status. 

The dataset is included in GS_Score_byWord_updated.csv

1. For each stimulus, identify pairs of words from each subject's data that are within IU boundaries and across IU boundaries, based on IU Position.
2. Add a column to note if they are within or across boundaries. 
3. Grab the Correct (yes/no) column data for those pairs of words. 
4. 
5. Code these pairs as "Matching" (both "yes" or both "no" / sum = 0 or 2 ) or "Not Matching" (one "yes" , one "no", sum = 1)
"""

import numpy as np
import pandas as pd
import statsmodels
import pylab

"""Read in file containing the automatically scored results 
of memory experiment. Each row in the table represents the score 
(Correct = 0 or 1)  for one word from one stimulus for one subject.
There are 101 subjs * 54 stimuli * sum of words in all stimuli = 203818 rows total """
scores = pd.read_csv('/Users/heathersimpson/Documents/Dissertation/Experiment1/Data/GS_Score_byWord_updated.csv', sep='\t')
"""
Recode the Correct column as binary integer values (0/1)
"""
scores['Correct'] = np.where(scores['Correct']=='yes', 1, 0)
"""Group the dataframe by stimulus, so that the scores for each word by subject 
will be easier to compare  
"""
grouped = scores.groupby('StimulusID')



#==============================================================================
# Step 1:  Getting word pairs 
#==============================================================================
#%%
#for stimulus in scores['StimulusID'].unique()
stimulus = 0 # ID for stimulus 0, ('Stimulus ID' values are integers 0-53)
stimscores = grouped.get_group(stimulus) #get_group takes label as argument, so variable stimulus should = valid StimulusID value 
stimscores['WordPosition'].max() #find the max WordPosition so that it can be used to constrain the 

"""find the rows n and n+1 where ['IUPosition'] is equal, (within boundaries)
 and the rows n and n+1 where ['IUPosition;] is not equal (across boundaries)"""

"""def ReturnWordPairs: A function to return values for sequences of 2 words from 
the same Subject
for a specified column from the dataframe
"""
def ReturnWordPairs(scoresbystim, colname):  
  count = 0
  pairvals = []
  while count < len(scoresbystim):
    for n in range(len(scoresbystim)):
      curr_pairvals = scoresbystim.iloc[n:n+2] #access two rows in sequence, range with : is exclusive of the last number so use n+2
      if len(curr_pairvals['Subj'].unique())==1 and len(curr_pairvals['StimulusID'].unique())==1: #the above line checks that the Subject and Stimulus ID values are the same for both words, 
      #so we don't compare words across subjects and stimuli. This way, the entire scores dataframe could be
    #used if desired, rather than having to group it by subject or stimuli 
        pairvals.append(curr_pairvals[colname].values)
      count += 1
      print count
  if len(scoresbystim)/2 == (len(scoresbystim)-1)/2: #check if the dataset length is odd, if so the last value will be a list of only 1, so remove it 
    pairvals = pairvals[:-1]
  return pairvals #returns list of arrays, each containing the list of paired col values
#%%
#==============================================================================
# Step 2. Extract Matching status for each pair
#==============================================================================
"""
Create Match Status column that indicates, for each sequence of 2 words that a subject heard, whether: 
they were both forgotten (Correct = 0, 0)
they were both remembered (Correct = 1, 1)
or 
they don't match in their status (Correct = 0, 1 or 1,0)
"""
MatchStatus = []  
i = 0
for vals in ReturnWordPairs(stimscores, 'Correct'):
    if vals[0]+vals[1]==0:
        MatchStatus.append("bothforgotten")
    elif vals[0]+vals[1]==2:
        MatchStatus.append("bothremembered")
    elif vals[0]+vals[1]==1:
        MatchStatus.append("no match")
    else:
        print ("Error: At position %d of the returned word pairs list the sum of Correct Values is a number other than 0, 1, or 2" % i)
    i +=1
#%%
#==============================================================================
# Step 3. Extract IUPosition status for each pair
#==============================================================================

IUStatus = []  
i = 0
for vals in ReturnWordPairs(stimscores, 'IUPosition'):
    if vals[0]==vals[1]:
        IUStatus.append("withinIU")
    else: 
        IUStatus.append("acrossIU")      



