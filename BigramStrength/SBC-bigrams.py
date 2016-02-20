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
for w in text:
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
#Splitting Up Words with Dashes
    
#I'm splitting up 'words' in the corpus that contain dashes. This is the multi-digit numbers that are treated as one word in parsed stimuli and multiple words in stimulus text (e.g. 'three-quarter-inch', 'seventy-two')
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

#My script that originally processed the SBC corpus before identifying my stimuli had removed dashes, turning dash-separated words like "three-quarter-inch" into "threequarterinch". I then individually separated those numbers into separate words in a script that processed the stimuli in a later step.

#Loading in stimuli dataset
GSstim = pd.read_csv("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/GS_Score_byWord_updated.csv", sep='\t')
[w for w in GSstim['Word'].values if re.search('-', w)]
#results in empty list, so we are good

##To view some of the offending values:
for t in text:
   if re.search(r'-', t[0]):
       print t

#Tested this out before I ran it: 
x = [('five', 'NN'), ('twenty-eight', 'JJ'), ('boo', 'NJ'), ('sixty-eight', 'NN')]
position = 0
for y in x: 
    print y
    print position
    if re.search(r'\w-\w',y[0]):
        print "Removed "+str(x.pop(position))+" " + str(position) #remove tuple t from text
        new_words = y[0].split('-')
        for i in range(len(new_words)): #
            print "New Words Position: "+ str(i)
            newtuple = (new_words[i], y[1]) #Each new tuple uses same POS tag (t[1])
            x.insert(position+i, newtuple)
    position+=1
#Looks good!
    
#Split words separated by a dash into separate words
    #This will take care of the words like "ninety-sixes" that had to be specially treated in GetPOSTagsforWordPairs.ipynb
position = 0
for t in text: 
    if t[0] == "double-u":
        text[position] = ("doubleu", t[1])
    elif re.search(r'\w-\w',t[0]):
        print "Removed " + str(text.pop(position))+ " " + str(position) #remove tuple t from text
        new_words = t[0].split('-')
        for i in range(len(new_words)): 
            newtuple = (new_words[i], t[1]) #Each new tuple uses same POS tag (t[1])
            text.insert(position+i, newtuple)
    position+=1
    
#==============================================================================  

text = [(w,p) for w,p in text if re.match(r"[\'a-z]",w[0])]

nonlemwords = [w for w,p in text]
#==============================================================================
# Create non-lemmatized version to use if the lemmatized version doesn't have matches (because of differences in POS tagging)
#==============================================================================
bigrams = FreqDist(zip(nonlemwords[:-1],nonlemwords[1:]))
unigram = FreqDist(nonlemwords)

sbig = float(sum(bigrams.values()))
suni = float(sum(unigram.values()))

nonlemassoc = {}
for b0,b1 in bigrams:
    p1 = unigram[b0]/suni
    p2 = unigram[b1]/suni
    p12 = bigrams[b0,b1]/sbig
    nonlemassoc[b0,b1] = log(p12)-log(p1)-log(p2) 
#==============================================================================
# #Write SBC Bigram association scores to file
#==============================================================================
f=open("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/BigramStrength/SBC-nonlembigrams.txt","w")
#Give it headers first
f.write("Word1\tWord2\tpwMI\n")
f.close()

f=open("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/BigramStrength/SBC-nonlembigrams.txt","a")
for w1,w2 in nonlemassoc:
    f.write(w1+"\t"+w2+"\t"+str(nonlemassoc[w1,w2])+"\n")
f.close()

#==============================================================================
#Lemmatize then calculate pointwise mutual information
#==============================================================================
            
wnl = WordNetLemmatizer()

words = []
for w,p in text:
    if p[0]=="N":
        words += [wnl.lemmatize(w,"n")]
    elif p[0]=="V":
        words += [wnl.lemmatize(w,"v")]
    else:
        words+=[w]
        
bigrams = FreqDist(zip(words[:-1],words[1:]))
unigram = FreqDist(words)

sbig = float(sum(bigrams.values()))
suni = float(sum(unigram.values()))

assoc = {}
for b0,b1 in bigrams:
    p1 = unigram[b0]/suni
    p2 = unigram[b1]/suni
    p12 = bigrams[b0,b1]/sbig
    assoc[b0,b1] = log(p12)-log(p1)-log(p2) 

#==============================================================================
# #Write SBC Bigram association scores to file
#==============================================================================
f=open("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/BigramStrength/SBC-bigrams.txt","w")
#Give it headers first
f.write("Word1\tWord2\tpwMI\n")
f.close()

f=open("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/BigramStrength/SBC-bigrams.txt","a")
for w1,w2 in assoc:
    f.write(w1+"\t"+w2+"\t"+str(assoc[w1,w2])+"\n")
f.close()