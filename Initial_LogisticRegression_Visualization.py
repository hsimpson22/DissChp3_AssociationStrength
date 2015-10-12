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
import seaborn as sns

#%%
#==============================================================================
# Saving Plots 
#==============================================================================

# define function to save any plots created below (credit for this function goes to: http://www.jesshamrick.com/2012/09/03/saving-figures-from-pyplot/)
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
# Read in Data
#==============================================================================

#Read in CSV
pairsdf = pd.read_csv('WordPairsScores.csv', sep='\t', index_col=0)

#Fix 'WithinIU' variable so its 0/1 values  matches 'ClauseBoundary' variable (right now they mean the opposite , 0 = boundary vs. no boundary )
pairsdf['IUBoundary']=[0 if pairsdf.WithinIU.loc[i]==1 else 1 for i in range(len(pairsdf.WithinIU))]
#==============================================================================
# Create Variable for IU vs. Clause Boundary Status
#==============================================================================
#Change structure so now we are using Boundary variable as Dependent variable, with type of boundary ("IU" or "Clause") as independent variable

#Create Boundary status variable 
Boundary = [1 if pairsdf.ClauseBoundary[i]==1 or pairsdf.WithinIU[i]==0 else 0 for i in range(len(pairsdf))]

#Create Boundary Type variable in two steps

#First just create values for Clause  
BoundaryType = ["Clause" if pairsdf.ClauseBoundary[i]==1 else "None" for i in range(len(pairsdf))]
#Then add "IU" value where Clause doesn't have a boundary, and rewrite with "Both" where Clause does have boundary
for i in range(len(BoundaryType)):
    if pairsdf.WithinIU[i]==0:
        if BoundaryType[i]=="Clause":
            BoundaryType[i]="Both"
        else:
            BoundaryType[i]="IU"

pairsdf['Boundary']=Boundary
pairsdf['BoundaryType']=BoundaryType

pairsdf['BoundaryType'].value_counts()

sns.countplot(x="BoundaryType", data=pairsdf[(pairsdf.Boundary==1) & (pairsdf.Subject==0)], order=['IU', 'Clause', 'Both'])
save("BoundaryTypeBreakdown", ext="png",close=True, verbose=True)

#==============================================================================
# Logistic Regression for IU and Clause Boundaries
#==============================================================================


#make dummy variables for 4 value variable BoundaryType, use "None" as the reference value
dummyBoundTypes = pd.get_dummies(pairsdf['BoundaryType'])

cols_to_keep = ['Matching', 'WordPosition', 'WCount']
IUClause_df = pairsdf[cols_to_keep].join(dummyBoundTypes.ix[:,:'IU'])

IUClause_df['Intercept']= 1.0

IUClause_df_logit = sm.Logit(IUClause_df.Matching, IUClause_df[IUClause_df.columns[1:]])
IUClause_df_result = IUClause_df_logit.fit()
print IUClause_df_result.summary()

#All the coefficients are negative, so 

#Now let's try creating new dataframe, getting rid of values where there is both a Clause and IU boundary 

pairsdf_noboth=pairsdf[pairsdf.BoundaryType!="Both"]
cols_to_keep = ['Matching', 'WithinIU', 'WordPosition', 'WCount']
pairsdf_noboth = pairsdf[cols_to_keep].join(dummyBoundTypes.ix[:,:'IU'])

pairsdf_noboth['Intercept']= 1.0

noboth_logit = sm.Logit(pairsdf_noboth.Matching, pairsdf_noboth[pairsdf_noboth.columns[1:]])
noboth_result = noboth_logit.fit()
print noboth_result.summary()


#

#==============================================================================
# Logistic Regression for IU Boundary Status only
#==============================================================================
#create a new dataframe just for the regression

IUonly_df = pd.DataFrame(data={'Matching':pairsdf.Matching, 'WithinIU':pairsdf.WithinIU, 'WordPosition':pairsdf.WordPosition, 'WordCount':pairsdf.WCount})

#add the intercept
IUonly_df['intercept']= 1.0

logit = sm.Logit(IUonly_df.Matching, IUonly_df[IUonly_df.columns[1:]])
result = logit.fit()
print result.summary()
#psuedo Rsquarted 

#odds ratio
np.exp(result.params) #this is supposed to be how much a 1 unit change in the IV variable affects the dep. variable, though not as clearly interpretable for a binary DV

#==============================================================================
#   Data Visualization
#==============================================================================
#playing around with data visualization using the seaborn package

sns.violinplot(x="WCount", y="IUStatus", hue="MatchStatus", data=pairsdf) 
#not really informative because it is showing the density of datapoints, but 
sns.countplot(x="MatchStatus", data=pairsdf, hue = "IUStatus")
save("countplot_MatchStatus", ext="png",close=True, verbose=True)

