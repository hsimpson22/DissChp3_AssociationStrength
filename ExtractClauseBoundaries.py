# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:20:21 2015

@author: heathersimpson
"""

"""
This script will extract within / across Clause boundary information for words in my memory experiment stimuli. Clause information will be taken from parse trees created for each stimulus with the Stanford parser.
"""
import os
import re
from nltk.grammar import Production, CFG, is_terminal, Nonterminal
from nltk.tree import Tree
#Step through parsed trees, identifying words, collect all tags before each word
f = open("/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_MutualInfoIUboundaries/Stimuli_StanfordParses.txt", 'r')
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

#Fix up the last tree in stimulus 0.. stimulus 0 excluded the last IU (="stating that") in the speaker's turn, to make it fit with the desired IU count. Those two words were included in the text given to the parser in case the omission would have caused the parser difficulty, but we don't want to include them in our analysis since the subjects didn't actually hear them.. I removed those two words from the stanford parse tree text file that we read in earlier, but now I need to add in the final parentheses to make the parse processable by the Tree function
stimtrees[5] = (re.sub(r'\n\n$', '',stimtrees[5][0]),stimtrees[5][1]) #first remove newlines from end so we can add the closing parentheses in the right place (right after "state") 
stimtrees[5] = (stimtrees[5][0]+")))))))\n(. ?))\n(. .)))\n\n",stimtrees[5][1])

processed_trees = [Tree.fromstring(tree[0]) for tree in stimtrees] #create Tree structure and viewable tree image for each tree
processed_trees[0] # shows tree image for stimulus 0
#prods=[t.productions() for t in processed_trees]
rules = reduce(lambda x,y:x+y,[t.productions() for t in processed_trees])
mycfg= CFG(Nonterminal("ROOT"), rules)
mycfg.start()
mycfg.productions(lhs=Nonterminal("PP")) #Will print productions for the specified nonterminal item (e.g. "PP", a prepositional phrase), where the PP is the left-hand side of the rule (e.g. PP -> whatever)

mycfg.is_leftcorner(Nonterminal("S"), "I")
#Output Clause begin status for each word (YES if it's the first word after the S tag) 
#I will do one with SBAR and one with S.. SBAR indicates a complementizer or adverbial that introduces a subordinate clause, the SBAR node may be empty



#Beginning of Stimulus marked as so: 

#have to join any separated contractions, e.g. "That   's"