# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:20:21 2015

@author: heathersimpson
"""

"""
This script will extract within / across Clause boundary information for words in my memory experiment stimuli. 

Clause information will be taken from parse trees created for each stimulus with the Stanford parser.
"""
import os
import re
from nltk.grammar import Production, CFG, is_terminal, Nonterminal
from nltk.tree import Tree
import numpy as np
import pandas as pd
#Step through parsed trees, identifying words, collect all tags before each word
f = open("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/Stimuli_StanfordParses.txt", 'r')
stanfordparsefile = f.read()  # read in the file as a single string, because we don't want to split by newlines, since one parse spans multiple lines, and the file is small enough that we can read it in this way
f.close()
splitbystim = re.split(r'\s*\<STIM[^>]+\>\s*', stanfordparsefile) # split up by the tags I manually inserted in this file to indicate stimulus boundaries (<STIM 0 TURN BEG>, <STIM 0 TURN END>)
splitbystim = filter(None, splitbystim) #Removes empty strings from the list

#Remove dependency parses (e.g. advmod(when-3, when-2), \nneg(know-17, n't-16)) that appear below each tree
treesonly = [re.sub(r'[^|\n]\w+\([^\s\)]+\-\d+.?\,\s*[^\s\)]+\-\d+.?\)\n*', '', stim) for stim in splitbystim]
#remove <TURN> tags
treesonly = [re.sub(r'\n*\<TURN\>\n*', '', stim) for stim in treesonly]

#Some of the stimuli have multiple parse trees, split those up (ROOT is the starting value)
stimtrees=[]
for t in treesonly:
    num = treesonly.index(t) #save position index so we know what stimulus the tree is from (pos 0 = stim id 0)
    r = re.split(r'\(ROOT',t) #split by ROOT tag
    for m in r:
        if m !='':
            stimtrees.append(("(ROOT"+m, num)) #add ROOT tag back at the beginning of the tree, and output a tuple with tree and the stimulus ID (num)

"""Fix up the last tree in stimulus 0.. stimulus 0 excluded the last IU (="stating that") in the speaker's turn, to make it fit with the desired IU count. Those two words were included in the text given to the parser in case the omission would have caused the parser difficulty, but we don't want to include them in our analysis since the subjects didn't actually hear them.. I removed those two words from the stanford parse tree text file that we read in earlier, but now I need to add in the final parentheses to make the parse processable by the Tree function
"""
stimtrees[5] = (stimtrees[5][0]+")))))))\n(. ?))\n(. .)))\n\n",stimtrees[5][1])

processed_trees = [Tree.fromstring(tree[0]) for tree in stimtrees] #create Tree structure and viewable tree image for each tree
processed_trees[0] # shows tree image for stimulus 0
#prods=[t.productions() for t in processed_trees]
rules = reduce(lambda x,y:x+y,[t.productions() for t in processed_trees])
mycfg= CFG(Nonterminal("ROOT"), rules)
mycfg.start()
mycfg.productions(lhs=Nonterminal("PP")) #Will print productions for the specified nonterminal item (e.g. "PP", a prepositional phrase), where the PP is the left-hand side of the rule (e.g. PP -> whatever)

#%%
#==============================================================================
# Loop through Production rules to extract Syntactic Tags and Terminal Words, keep track of Clause boundaries by looking for the first word appearing after an "S" tag
#==============================================================================
words = []
counter = 0
tags = []
ruleset=[]
ClauseBoundary = False #below, this variable will be set to TRUE if the rule begins with 'S' (clause boundary), or FALSE the rule contains a terminal 
for rule in rules:
    print counter 
    tags.append(str(rule.lhs())) #store left-hand side syntactic category, this will create some duplicates in the tag set since sometimes it was already included in right hand side of previous rule, but we don't need to care about that
    ruleset.append(rule)
    rightside = rule.rhs() #
    if type(rightside[0])==str:
        if rightside[0] in ['.','?','\\/', '-LCB-','-RCB-','FOOTSTEPS']: #remove bad ones that I identified in previous run of this script
          tags = [] 
          ruleset = []
          ClauseBoundary = False
        else:
            word = rightside[0] #store the word so it can be added to words output list
            mini_cfg=CFG(Nonterminal("ROOT"), ruleset)
            if mini_cfg.is_leftcorner(Nonterminal('S'), word):
                ClauseBoundary = True
            words.append((tags, word,ClauseBoundary))
            tags = [] 
            ruleset = []
            ClauseBoundary = False   
    else: 
# if the rule is not terminal (meaning rhs is another syntactic category tag like "NP")
        tags.extend([str(r) for r in rightside])
    counter +=1
            
        
#%%
        
#==============================================================================
# Identify Words that were split up by the parser: 
        #contractions with apostrophes "they'll"
        #modals "gonna" , "wanna" 
   #put them back together
#==============================================================================
position = []
count = 0
fixedcontractions = []
contractions = []
for w in words:  #so we are editing the list created in previous cell, that might be bad practice? but efficient bc it doesn't require creation of new list with almost all the same elements
  if re.search(r'[^o]?\'[^c]', w[1]) or re.search(r'^na$', w[1]): #match the apostrophe in split contractions, the NOT 'o' and NOT 'c' are there to exclude 'o'clock'   
    combinedtags = words[count-1][0]+w[0]
    combinedwords = words[count-1][1]+w[1]
    if words[count-1][2] or w[2]:
      combinedclause = True #Set the Clause boundary status to "True" if either of the elements are True
    else: 
      combinedclause = False
    newtuple = (combinedtags,combinedwords,combinedclause)
    words[count-1]=newtuple # replace tuple at the previous position (first half of the contraction) with new joined elements, will remove the 2nd half of the contraction later
    fixedcontractions.append(newtuple) #save the new tuples for review
    contractions.append(w) #save list of contractions to use them in later removal step (matching the value in words)
    position.append(count)
  count+=1
  
#Editing the Words list to remove elements  
#Remove Contractions
wl = len(words)
[words.remove(c) for c in contractions] # remove the second half of the contraction from the list 
if wl-len(words)!=len(contractions): #check to make sure it removed correct amount
    print ("Removal step removed %d, should have removed %d" % wl-len(words), len(contractions))

#%% 
#==============================================================================
# Check for any additional not matching words
#==============================================================================
scores = pd.read_csv('./GS_Score_byWord_updated.csv', sep='\t') #The file containing the rest of the experiment data, we need to make sure that the list of words we've extracted from the syntactic parses matches the list of words here, so that we can match up their values for ClauseBoundary 
bysubj = scores.groupby('Subj')
subj0 = bysubj.get_group(0)
scores_words = subj0['Word'].values 
#len(scores_words) is smaller than len(words), so we still probably have some funky stuff going on (probably leftover punctuation that was treated as strings)
#%%
#Let's compare to see what remaining word strings are in words that aren't in scores_words
scores_set = set(scores_words) 
diffwords=[y for x,y,z in words if y not in scores_set];diffwords

#['o',
# 'threequarterinch',
# 'threequarter',
# 'thirtyone',
# 'seventytwo',
# 'twentyeight',
# 'ninetyeights',
# 'ninetysixes',
# 'ninetynine']

#==============================================================================
# Fix the rest of not matching words:
  #1. 'o' in stimulus 4 "fear is so crippling", in original text it was -o but clearly sounds like 'so' so I changed it in the scoring representation
  
  #2. multi-digit numbers that are treated as one word in parsed stimuli and multiple words in stimulus text (e.g. 'threequarterinch', 'seventytwo')
    
#==============================================================================
#%%
#First fix 'o' -> 'so' in Stim 4 
[i for i,x in enumerate(words) if x[1] =='o'] # found 'o' is at position [341]
words[341]=(words[341][0], 'so' , words[341][2]) #have to replace the entire tuple since we can't edit tuple elements

#Update diffwords
diffwords=[y for x,y,z in words if y not in scores_set]; diffwords
# 'threequarterinch',
# 'threequarter',
# 'thirtyone',
# 'seventytwo',
# 'twentyeight',
# 'ninetyeights',
# 'ninetysixes',
# 'ninetynine']

#Fix number elements, need to split up into multiple entries

#find values for the elements to fix
fix_num_values = [x for x in words if x[1] in diffwords]

#make sure the resulting list of positions has a one-to-one correspondence with diffwords
if len(fix_num_values) != len(diffwords): 
    print "Lengths of lists to fix do not match"  

#If nothing, then we can move on to fixing these values
#Note that we have to search for each position separately as we start changing values because we will be messing with the number of elements in the list. 

#%%
#Let's define a little function to split and insert new elements 
def SplitValues(position, values, wordslist): #*value would be list of new values for 
    newtuple =(wordslist[position][0], values[0], wordslist[position][2]) 
    wordslist[position] = newtuple
    if len(values)>1:
        for i in range(1,len(values)):
            nexttuple = (newtuple[0], values[i], newtuple[2])
            wordslist.insert(position+i, nexttuple)    

#%%

#==============================================================================
# Fix number values 

#I'm stepping through each one by one, I didn't do this with a loop because I wanted to  be really careful and clear about the values that I'm changing instead of making it one big list of lists that would be hard to read
#==============================================================================

# 'threequarterinch'
pos = [i for i, x in enumerate(words) if x[1] =='threequarterinch'][0] 
SplitValues(pos, ['three', 'quarter', 'inch'], words)

# 'threequarter',
pos = [i for i, x in enumerate(words) if x[1] =='threequarter'][0] 
SplitValues(pos, ['three', 'quarter'], words)
# 'thirtyone',
pos = [i for i, x in enumerate(words) if x[1] =='thirtyone'][0] 
SplitValues(pos, ['thirty', 'one'], words)

# 'seventytwo',
pos = [i for i, x in enumerate(words) if x[1] =='seventytwo'][0] 
SplitValues(pos, ['seventy', 'two'], words)

# 'twentyeight',
pos = [i for i, x in enumerate(words) if x[1] =='twentyeight'][0] 
SplitValues(pos, ['twenty', 'eight'], words)

# 'ninetyeights',
pos = [i for i, x in enumerate(words) if x[1] =='ninetyeights'][0] 
SplitValues(pos, ['ninety', 'eights'], words)

# 'ninetysixes',
pos = [i for i, x in enumerate(words) if x[1] =='ninetysixes'][0] 
SplitValues(pos, ['ninety', 'sixes'], words)

# 'ninetynine']
pos = [i for i, x in enumerate(words) if x[1] =='ninetynine'][0] 
SplitValues(pos, ['ninety', 'nine'], words)

#check on word diffs again
diffwords=[y for x,y,z in words if y not in scores_set]
if bool(diffwords) == False: 
    print "No diffs between words and set(GS_scores_words)"
#There are no diffs!

#Now check for differences the other way, see if there are any words in GSscores that aren't in words set
wordsset = set([y for x,y,z in words])
diffwords2 = [y for w in scores_words if w not in wordsset]
if bool(diffwords2)==True:
    print ("Need to reconcile diffs, there are %d words in the Clause boundary set that aren't in GS scores set" % len(diffwords2))
else:
    print "No diffs between Clause boundary word set and GS Scores word set! Proceed to next step!"
#also empty!
#%%
# Now we need to check that the lists are exactly the same
# We just checked that the unique word values are the same, we did that first because it is faster, but there could be a word that is in both sets, but appears more times in one set than the other" 

len(subj0)==len(words) #False! So we need to figure out which words are different by checking every element in the list

#I'l have it through comparing the lists, then stop 

def checkforDiffs(list1, list2): #list1 here is words, list2 is subj0.Word
  i = 0
  while i<len(list2):
      if list1[i][1]!=list(list2)[i]: break #I have to change subj0.Word to a list here because it is a subset of a dataframe and keeps the row indexes from the original dataframe, which was organized by stimulus so when we go to the next stim for same subject, we've skipped about 1000 rows so it throws an index error      
      else:
          print ("Matched at pos %d" %i)
      i+=1
  if i<len(list2):
      print str(i) + " " + list1[i][1] + "  " + list(list2)[i]
  else: 
      print "Reached end oflist2"

#First diff: 1344 Okay I've
checkforDiffs(words, subj0.Word)
[y for x, y, z in words[1342:1347]]
list(subj0.Word)[1342:1347] #"Okay" missing from GSscores Word list. Will remove from words
words.pop(1344) #Removed (['ROOT', 'INTJ', 'INTJ', 'UH', '.', 'UH'], 'Okay', False)

#2nd diff: 1574 Right Yeah
checkforDiffs(words, subj0.Word)
[y for x, y, z in words[1572:1577]]  #['of', 'me', 'Right', 'Yeah', 'but']
list(subj0.Word)[1572:1577]  # ['of', 'me', 'Yeah', 'but', 'then']
#"Right" missing from GSscores word list, will remove from words
#I think I removed these items because I believed them to be mistakes in the transcription, and they didn't make a difference in the # of clauses, but I will need to go back and double-check this. Why did you not document this better, 2-years-ago-me?? 
words.pop(1574) #Removed (['ROOT', 'ADVP', 'ADVP', 'RB', '.', 'RB'], 'Right', False)

checkforDiffs(words, subj0.Word) 
#All matched, alright!

#%%
#==============================================================================
# Create DataFrame with Clause Boundary status 
#==============================================================================

ClauseStatus_df = pd.DataFrame(data=words, columns=['Tags', 'Word','ClauseBoundary'])
ClauseStatus_df['StimID']=subj0['StimulusID'].values
#Export CSV
pd.DataFrame.to_csv(ClauseStatus_df, path_or_buf="./ClauseBoundaryInfo.csv", sep='\t', columns=ClauseStatus_df.columns)

#Output Clause begin status for each word (YES if it's the first word after the S tag) 
#I will do one with SBAR and one with S.. SBAR indicates a complementizer or adverbial that introduces a subordinate clause, the SBAR node may be empty
