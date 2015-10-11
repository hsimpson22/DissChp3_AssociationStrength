# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 15:36:09 2015

@author: heathersimpson
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import matplotlib.pyplot as plt
#Read in CSV
pairsdf = pd.read_csv('WordPairsScores.csv', sep='\t', index_col=0)

#%%
#==============================================================================
# Initial Logistic Regression Analysis
#==============================================================================


#create a new dataframe just for the regression


df_logit = pd.DataFrame(data={'Match':pairsdf.Matching, 'WithinIU':pairsdf.WithinIU, 'WordPosition':pairsdf.WordPosition, 'WordCount':pairsdf.WCount})

#add the intercept
df_logit['intercept']= 1.0

logit = sm.Logit(df_logit.Match, df_logit[df_logit.columns[1:]])
result = logit.fit()
print result.summary()
#psuedo Rsquarted 

#odds ratio
np.exp(result.params) #this is supposed to be how much a 1 unit change in the IV variable affects the dep. variable, though not as clearly interpretable for a binary DV

#%%
#==============================================================================
# Saving Plots 
#==============================================================================

# define function to save plots (credit for this function goes to: http://www.jesshamrick.com/2012/09/03/saving-figures-from-pyplot/)
def save(path, ext='png',close=True, verbose=True):
  """ path = string to save the file to, ext = file extension, default = png
  """
  directory = os.path.split(path)[0]
  filename = "%s.%s" %(os.path.split(path)[1], ext)
  if directory == '':
      directory = '.'
  #if directory does not exist, create it
  if not os.path.exists(directory):
      os.makedirs(directory)
  #the final path to save to
  savepath = os.path.join(directory, filename)
  #print info about where it saved if verbose
  if verbose: 
      print("Saving figure to '%s' ..." % savepath),
  #save the figure  
  plt.savefig(savepath)
  
  if close:
      plt.close()
  if verbose:
      print("Done")

#%%
#==============================================================================
#   Data Visualization
#==============================================================================
#playing around with data visualization using the seaborn package
import seaborn as sns
sns.violinplot(x="WCount", y="IUStatus", hue="MatchStatus", data=pairsdf) 
#not really informative because it is showing the density of datapoints, but 
sns.countplot(x="MatchStatus", data=pairsdf, hue = "IUStatus")
save("countplot_MatchStatus", ext="png",close=True, verbose=True)