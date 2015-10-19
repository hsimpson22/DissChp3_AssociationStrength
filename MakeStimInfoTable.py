# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 18:17:50 2015

@author: heathersimpson
"""

import os
import re
import numpy as np
import pandas as pd

#File with SBC filename, start / end time, Speaker name
exp1stim = pd.read_csv("/Users/heathersimpson/Documents/Dissertation/Experiment1/Experiment1_Stimuli.csv", sep="\t")
m = [re.match(r"([\d\.]+)\_([\d\.]+)\_(\w+)", v) for v in exp1stim.TurnInfo.values]
start = [v.group(1) for v in m]
start = [round(float(x), 2) for x in start]
end = [v.group(2) for v in m]
end = [round(float(x), 2) for x in end]
speaker = exp1stim.Speaker.values

stimcat = exp1stim.CandidateFor.values #This gets us the category for the stimulus based on size in various units (it's supposed to have 2 examples each for the permutation of 'H' high, 'M' medium, 'l' low counts for word, IUs, Clauses )

m = [re.match(r"(sbc\d+)\_.*Rprep", v) for v in exp1stim.TurnFile.values]
sbcfile = [v.group(1) for v in m]
#File with Word, IU, Clause Count and Mean / Max % score
percCorrect = pd.read_csv("/Users/heathersimpson/Documents/Dissertation/Experiment1/Data/DissExp1_AllStimuli_PercCorrectbyStimulus.csv", sep="\t")

percCorrect.columns
meanCorrect = percCorrect.groupby('StimID').aggregate(np.mean).PercCorrect.values
meanCorrect = [round(x*100, 1) for x in meanCorrect]
maxCorrect = percCorrect.groupby('StimID').aggregate(np.max).PercCorrect.values
maxCorrect = [round(x*100, 1) for x in maxCorrect]

grouped = percCorrect.groupby('Subject')

#get values for StimID , Words, IUs, Clauses
stimID = grouped.get_group(0).StimID.values
words = grouped.get_group(0).Words.values
ius = grouped.get_group(0).IUs.values
clauses = grouped.get_group(0).Clauses.values
duration = grouped.get_group(0).StimDur.values
duration = [round(x, 2) for x in duration]
#==============================================================================
# Create strings in LaTeX table format

#Desired Output: 

#First line: 
#Stimulus & SBC filename & Start Time & End Time & Duration & Speaker & Words & IUs & Clauses & Mean % correct & Max % correct \\

#Rest of lines: 
#stimID & stimcat & sbcfile & start & end & duration & speaker & words & ius & clauses & meanCorrect & maxCorrect
#==============================================================================


stiminfo = "Stimulus & SBC filename & Start Time & End Time & Duration & Speaker & Words & IUs & Clauses & Mean \% Correct & Max \% Correct \\\\ \n"
for i in range(54):
    stiminfo += str(stimID[i]) + " & " + str(sbcfile[i]) + " & " + str(start[i]) + " & " + str(end[i]) + " & " + str(duration[i]) + " & " + str(speaker[i]) + " & " + str(words[i]) + " & " + str(ius[i]) + " & " + str(clauses[i]) + " & " + str(meanCorrect[i]) + " & " + str(maxCorrect[i]) + "\\\\ \n"

stiminfofile = open('stiminfo.txt', 'w')
stiminfofile.write(stiminfo)
stiminfofile.close()