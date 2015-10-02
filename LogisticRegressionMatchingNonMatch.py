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

We will analyze this by looking at the effect of within/across boundary status on 
recall of pairs of words of distance 1. The prediction is that words across boundaries will 
tend not to match in their recall status, and that words within boundaries will tend to match.

The dataset is included in GS_Score_byWord_updated.csv

Overview of plan:
1. Identify 2-word sequences from each subject's data that are within IU boundaries and across IU boundaries, based on IU Position.
2. Add a column to note if they are within or across boundaries. 
3. Grab the Correct (yes/no) column data for those pairs of words. 
4. 
5. Code these pairs as "Matching" (both "yes" or both "no" / sum = 0 or 2 ) or "Not Matching" (one "yes" , one "no", sum = 1)
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import pylab as pl

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



#==============================================================================
# Step 1:  Getting word pairs 
#==============================================================================
#%%

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
  if len(pairvals[-1:]<2: #sometimes the final value may be of length 1, such as if the dataset length was odd. If so, remove that final value.
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
for vals in ReturnWordPairs(scores, 'Correct'):
    if vals[0]+vals[1]==0:
        MatchStatus.append("bothforgotten")
    elif vals[0]+vals[1]==2:
        MatchStatus.append("bothremembered")
    elif vals[0]+vals[1]==1:
        MatchStatus.append("no match")
    else:
        print ("Error: At position %d of the returned word pairs list the sum of Correct Values is a number other than 0, 1, or 2" % i)
    i +=1
    
 """Optional:  Group scores dataframe by Stimulus so that it is faster to process
I did this while I was testing: 

grouped = scores.groupby('StimulusID')
stimulus = 0 # ID for stimulus 0, ('Stimulus ID' values are integers 0-53)
stimscores = grouped.get_group(stimulus) #get_group takes label as argument, so variable stimulus should = valid StimulusID value 
"""
   
    
#%%
#==============================================================================
# Step 3. Extract IUPosition status for each pair
#==============================================================================

IUStatus = []  
i = 0
for vals in ReturnWordPairs(scores, 'IUPosition'):
    if vals[0]==vals[1]:
        IUStatus.append("withinIU")
    else: 
        IUStatus.append("acrossIU")      

"""Collect the other important values for the word pairs 
# Then, export full DataFrame as CSV so I can import into R for rest of stats because I 
# need to do a mixed effects logistic regression which is not supported in 
# Python and I don't want to deal with learning rpy2 at this moment
"""
#%%
#==============================================================================
# Subject
#==============================================================================

Subj = [] 
i = 0
for vals in ReturnWordPairs(scores, 'Subj'):
    if vals[0]==vals[1]:
        Subj.append(vals[0])
    else:
        print ("Error: At position %d of the returned word pairs list, the pair has cross Subj boundaries (Subjs are not equal)" % i)
    i +=1  #should show 203818 iterations from ReturnWordPairs, but Subj len=198364 (because of removing the last word in odd-numbered-word-length stimuli )

#%%
#==============================================================================
# Stimulus ID
#==============================================================================

StimID = [] 
i = 0
for vals in ReturnWordPairs(scores, 'StimulusID'):
    if vals[0]==vals[1]:
        StimID.append(vals[0])
    else:
        print ("Error: At position %d of the returned word pairs list, the pair has cross Stim boundaries (Stim IDs are not equal)" % i)
    i +=1  #should show 203818 iterations from ReturnWordPairs, but StimID len=198364 (because of removing the last word in odd-numbered-word-length stimuli )

#==============================================================================
# Word (String values, joined the two with a dash e.g. "Then-when")
#==============================================================================
#%%
Word = [] 
for vals in ReturnWordPairs(scores, 'Word'):
        Word.append("-".join(vals))
Word = Word[:-1]  # the last value of Word is only one word long, and it has a length 1 higher than other values



#==============================================================================
# Word Position and WordCount
#==============================================================================
#%%
"""Will make WordPosition a relative value by calculating 
the percentage of the total word count that the word positions
represent, in other words indicating what percentage of the way
through the stimulus are you at that point. 

Since the position numbering 0 = end of the stimulus / most recent word the subject heard, 
smaller values for word position/word count will actually mean a larger proportion, so to 
correct for that I will compute  1 - word position/word count.

First just return the means of the word pair's positions, 
Then after WordCount is done, update WordPosition to divide the
mean by the total word count
"""
WordPosition=[]    
for vals in ReturnWordPairs(scores,'WordPosition'):
    WordPosition.append(np.mean(vals))
WordPosition=WordPosition[:-1] #same issue as Word variable, one extra value at the end from the last item in the dataset

WordCount = [] 
i = 0
for vals in ReturnWordPairs(scores, 'WCount'):
    if vals[0]==vals[1]:
        WordCount.append(vals[0])
    else:
        print ("Error: At position %d of the returned word pairs list, the WCount values do not match" % i)
    i +=1  #should show 203818 iterations from ReturnWordPairs, but Subj len=198364 (because of removing the last word in odd-numbered-word-length stimuli )
RelWordPosition=map(lambda wp, wc: 1-(wp/wc), WordPosition, WordCount) #subtract by 1 so that the values do represent the percentage  

#%%
#==============================================================================
# Clause Count & IU Count
#==============================================================================
ClauseCount = [] 
i = 0
for vals in ReturnWordPairs(scores, 'CLCount'):
    if vals[0]==vals[1]:
        ClauseCount.append(vals[0])
    else:
        print ("Error: At position %d of the returned word pairs list, the CLCount values do not match" % i)
    i +=1  #should show 203818 iterations from ReturnWordPairs, but Subj len=198364 (because of removing the last word in odd-numbered-word-length stimuli )
IUCount = []
i = 0
for vals in ReturnWordPairs(scores, 'IUCount'):
    if vals[0]==vals[1]:
        IUCount.append(vals[0])
    else:
        print ("Error: At position %d of the returned word pairs list, the IUCount values do not match" % i)
    i +=1        
#==============================================================================
# Create DataFrame and Export CSV
#==============================================================================
#Create new dataframe with our new variables
pairsdf = pd.DataFrame(data={'MatchStatus':MatchStatus, 'IUStatus':IUStatus, 'Word':Word, 'WordPosition':RelWordPosition, 'CLCount':ClauseCount, 'IUCount':IUCount, 'WCount':WordCount, 'Subject':Subj, 'StimID':StimID})

#turn MatchStatus into binary variable and add to dataframe
pairsdf['Matching'] = np.where(pairsdf['MatchStatus']=='no match', 0, 1)
#turn IUStatus into binary integers and add to dataframe
pairsdf['WithinIU'] = np.where(pairsdf['IUStatus']=="withinIU", 1, 0)

#Export CSV
pd.DataFrame.to_csv(pairsdf, path_or_buf="./WordPairsScores.csv", sep='\t', columns=pairsdf.columns)


#%%
#==============================================================================
# Initial Logistic Regression Analysis
#==============================================================================


logit = sm.Logit(pairsdf['Matching'], pairsdf['WithinIU'])
result = logit.fit()
print result.summary()
#odds ratio
np.exp(result.params) #this is supposed to be how much a 1 unit change in the IV variable affects the dep. variable, though not as clearly interpretable for a binary DV
