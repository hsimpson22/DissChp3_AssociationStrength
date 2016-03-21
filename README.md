# DissChp3_AssociationStrength
Code and datasets for Chapter 3 of my dissertation:  analysis of the memory association strength for bigrams within and across important units in short clips of spoken English. I am testing the unithood of Intonation Units (a type of prosodic phrase) and clauses by seeing whether association strength is higher within or across their boundaries. Association strength is measured by the recall status of the words. Subjects were asked to listen to each clip and then type everything they heard from memory. If two words are strongly associated in memory, it is expected that they will have the same recall status (either remembered together or forgotten together). If one was remembered and one was forgotten, that is taken as an indicator of less strong association. Recall status was used as the independent variable of interest. Bigram association strength based on existing associations (pointwise mutual information) was also calculated from a corpus and included as a control. 

ExtractClauseBoundaries.py : Extracts clause boundaries from Stimuli_StanfordParses.txt, resulting info -> ClauseBoundaryInfo.csv

ExtractingWordPairsData.py: Takes the scoring and other info for single words from GS_Score_byWord_updated.csv (scored memory experiment responses) into info for pairs of words -> WordPairsScores.csv

Initial_LogisticRegression_Visualization.py : Playing around with Scipy logistic regression modeling and data visualization using Pandas and Seaborn

MakeStimInfoTable.py:  Script to extract stimulus metadata and put into LaTeX table format to use in Appendix of dissertation

MixedEffectsLogisticRegression.R: computes statistical model used in dissertation chapter

WordClustering.py - (unfinished) playing around with clustering of words by their likelihood of being remembered together
