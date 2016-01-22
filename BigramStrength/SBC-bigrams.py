# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:26:14 2016

@author: fermin

modified by: heathersimpson
"""

cdir = "/Users/heathersimpson/Documents/Dissertation/Articles/Chp4_SynPrimingIUs/PARSED"
from os import listdir
from nltk import Tree
from PCFG_utilities import PreterminalizeTree
import re
from nltk import WordNetLemmatizer,FreqDist
from numpy import sum,log
import pandas as pd

filelist = listdir(cdir)

text = []
for filename in filelist:
    if filename[-7:]==".parsed":
        f = open(cdir+"/"+filename,"r")
        lines = f.readlines()
        f.close()
        
        for l in lines:
            tree = Tree.fromstring(l[:-1].split("\t")[3])
            iu = tree.leaves()
            pos = PreterminalizeTree(tree).leaves()
            iu = [w.lower() for w in iu]
            text += zip(iu,pos)
#==============================================================================
#Identify Words that were split up by the parser: 
        #contractions with apostrophes "they'll"
        #modals "gonna" , "wanna" 
   #put them back together so that they will match the word pairs from my stimuli 
   # I did this when computing the clause boundaries from parsed data, so I will base this off what I did in ExtractClauseBoundaries.py
#==============================================================================
count = 0
secondhalfpositions = []
for w in text:  #so we are editing the list created in previous cell, that might be bad practice? but efficient bc it doesn't require creation of new list with almost all the same elements
  if re.search(r'[^o]?\'[^c]', w[0]) or re.search(r'^na$', w[0]): #match the apostrophe in split contractions, the NOT 'o' and NOT 'c' are there to exclude 'o'clock' 
     secondhalfpositions.append(count)
     combinedword = text[count-1][0]+w[0] #combine the two halves of the word
     combinedPOS = text[count-1][1]+"-"+w[1] #combine the two POS tags
     text[count-1]=(combinedword, combinedPOS)
  count+=1

#Remove all the second halves of the words from text
removed_count = 0
for p in secondhalfpositions:
    text.pop(p-removed_count)
    removed_count +=1
    
#==============================================================================
#Now, fix the multi-digit numbers that are treated as one word in parsed stimuli and multiple words in stimulus text (e.g. 'three-quarter-inch', 'seventy-two')
#(Note: In my parsed stimuli they have no dashes, so the task was different in ExtractClauseBoundaries)
#in the version of the full SBC corpus parsed files that we are using, they are separated with dashes, which is much easier because we can split on the dash instead of having to define the split for each word separately
# 'threequarterinch',
# 'threequarter',
# 'thirtyone',
# 'seventytwo',
# 'twentyeight',
# 'ninetyeights',
# 'ninetysixes',
# 'ninetynine']

#Make sure there are no other dashes already in my data

GSstim = pd.read_csv("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/GS_Score_byWord_updated.csv", sep='\t')
[w for w in GSstim['Word'].values if re.search('-', w)]
#results in empty list, so we are good

##To view some of the offending values:
#for t in text:
#    if re.search(r'inch', t[0]):
#        print t

#Let's define a little function to split and insert new elements 
def SplitValues(position, values, wordslist): #*value would be list of new values for 
    newtuple =(wordslist[position][0], values[0], wordslist[position][2]) 
    wordslist[position] = newtuple
    if len(values)>1:
        for i in range(1,len(values)):
            nexttuple = (newtuple[0], values[i], newtuple[2])
            wordslist.insert(position+i, nexttuple)    

#==============================================================================
# Fix number values 

#I'm stepping through each one by one, I didn't do this with a loop because I wanted to  be really careful and clear about the values that I'm changing instead of making it one big list of lists that would be hard to read
#==============================================================================

# 'threequarterinch'
pos = [i for i, x in enumerate(words) if x[1] =='threequarterinch'][0] 
SplitValues(pos, ['three', 'quarter', 'inch'], words)

#==============================================================================  
  
  
  
text = [(w,p) for w,p in text if re.match(r"[\'a-z]",w[0])]
            
wnl = WordNetLemmatizer()

text2 = []
for w,p in text:
    if p[0]=="N":
        text2 += [wnl.lemmatize(w,"n")]
    elif p[0]=="V":
        text2 += [wnl.lemmatize(w,"v")]
    else:
        text2+=[w]
        
bigrams = FreqDist(list(zip(text2[:-1],text2[1:])))
unigram = FreqDist(text2)

sbig = float(sum(list(bigrams.values())))
suni = float(sum(list(unigram.values())))

assoc = {}
for b0,b1 in bigrams:
    p1 = unigram[b0]/suni
    p2 = unigram[b1]/suni
    p12 = bigrams[b0,b1]/sbig
    assoc[b0,b1] = log(p12)-log(p1)-log(p2) 
    
f=open("heather-bigrams.txt","w",encoding="UTF8")
for w1,w2 in assoc:
    print(w1,w2,assoc[w1,w2],file=f)
f.close()