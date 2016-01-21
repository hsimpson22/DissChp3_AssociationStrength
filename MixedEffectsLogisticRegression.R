rm(list=ls(all=TRUE)) #
library(lmerTest)
library(effects)
library(MuMIn)

WordPairs<-read.table(file = "/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_IUvsClauseBoundaries/WordPairsScores.csv", sep="\t", quote = "", header = TRUE, comment.char="")
str(WordPairs)

WordPairs$IUBoundary<-WordPairs$WithinIU
WordPairs$IUBoundary[WordPairs$IUBoundary==0]<-"yes"
WordPairs$IUBoundary[WordPairs$IUBoundary==1]<-"no"
WordPairs$IUBoundary<-as.factor(WordPairs$IUBoundary)

WordPairs$ClauseBoundary[WordPairs$ClauseBoundary==0]<-"no"
WordPairs$ClauseBoundary[WordPairs$ClauseBoundary==1]<-"yes"
WordPairs$ClauseBoundary<-as.factor(WordPairs$ClauseBoundary)
#====================================================================
#IU and Clause Boundary Mixed Effects Regression
#====================================================================
#both_glmm<-glmer(Matching ~ ((IUBoundary+ClauseBoundary)^2 + WordPosition + WCount + (1| Subject) + (1| StimID)), data= WordPairs, family = binomial)
#summary(both_glmm)
#WCount not significant (p value = 0.106) so removed
both_glmm2<-glmer(Matching ~ ((IUBoundary+ClauseBoundary)^2 + WordPosition + (1| Subject) + (1| StimID)), data= WordPairs, family = binomial)
summary(both_glmm2)
plot(allEffects(both_glmm2))
plot(Effect("IUBoundary", mod=both_glmm2),main="")
plot(Effect("ClauseBoundary", mod=both_glmm2),main="")
plot(Effect("WordPosition", mod=both_glmm2),main="")
plot(Effect(c("IUBoundary","ClauseBoundary"), mod=both_glmm2),main="")

#Association measures in nltk


r.squaredGLMM(both_glmm2) #measure Pseudo-R-squared using this function from the MuMIn library
#       R2m        R2c 
#0.02069033 0.09200276
#R2 m : Marginal R2 - variance explained by fixed factors#
#R2 c : conditional R2 - variance explained by fixed + random factors
#signma_f^2 variance / sigma f^2 + sum(sigma_l^2 + sigma e^2 + sigma d^2
#REMEMBER ONLY
rememberdata<-subset(WordPairs, MatchStatus!="bothforgotten", select=c(Matching, IUBoundary, ClauseBoundary, WordPosition, WCount, Subject, StimID))
remember_glmm<-glmer(Matching ~ ((IUBoundary+ClauseBoundary)^2 + WordPosition + WCount + (1| Subject) + (1| StimID)), data= rememberdata, family = binomial)
summary(remember_glmm)
plot(allEffects(remember_glmm))

forgottendata<-subset(WordPairs, MatchStatus!="bothremembered", select=c(Matching, IUBoundary, ClauseBoundary, WordPosition, WCount, Subject, StimID))
forgotten_glmm<-glmer(Matching ~ ((IUBoundary+ClauseBoundary)^2 + WordPosition + WCount + (1| Subject) + (1| StimID)), data= forgottendata, family = binomial)
summary(forgotten_glmm)
plot(allEffects(forgotten_glmm))





#====================================================================
#IU Boundary Only
#====================================================================
#Generalized Linear Mixed Model (binomial) on Matching = 0/1
glmm<-glmer(Matching ~ (IUBoundary + WordPosition + WCount + (1| Subject) + (1| StimID)), data= WordPairs, family = binomial)
summary(glmm)
# Generalized linear mixed model fit by maximum likelihood
# (Laplace Approximation) [glmerMod]
# Family: binomial  ( logit )
# Formula: 
#   Matching ~ (WithinIU + WordPosition + WCount + (1 | Subject) +  
#                 (1 | StimID))
# Data: WordPairs
# 
# AIC      BIC   logLik deviance df.resid 
# 181443.2 181504.4 -90715.6 181431.2   198358 
# 
# Scaled residuals: 
#   Min      1Q  Median      3Q     Max 
# -4.6386  0.3317  0.4094  0.4988  1.1878 
# 
# Random effects:
#   Groups  Name        Variance Std.Dev.
# Subject (Intercept) 0.02149  0.1466  
# StimID  (Intercept) 0.22283  0.4721  
# Number of obs: 198364, groups:  Subject, 101; StimID, 54
# 
# Fixed effects:
#   Estimate Std. Error z value Pr(>|z|)    
# (Intercept)   1.022168   0.116506    8.77   <2e-16 ***
#   WithinIU      0.628968   0.013790   45.61   <2e-16 ***
#   WordPosition -0.352042   0.021291  -16.53   <2e-16 ***
#   WCount        0.004028   0.002508    1.61    0.108    
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Correlation of Fixed Effects:
#   (Intr) WthnIU WrdPst
# WithinIU    -0.080              
# WordPositin -0.076 -0.072       
# WCount      -0.812 -0.001 -0.007
plot(allEffects(glmm))

#REMEMBERED ONLY
#But high volume of both forgotten datapoints within IU are inflating this effect, and they may indicate salience of words at IU boundaries as opposed to within IUs, rather than the unithood of IU representation. So will try again with only the remembered vs. non-matching

#subset the data for those two things
rememberdata<-subset(WordPairs, MatchStatus!="bothforgotten", select=c(Matching, MatchStatus, IUBoundary, WordPosition,WCount,Subject, StimID))
glmm2<-glmer(Matching ~ (IUBoundary + WordPosition + WCount + (1| Subject) + (1| StimID)), data= rememberdata, family = binomial)
summary(glmm2)
# Generalized linear mixed model fit by maximum likelihood (Laplace
#                                                           Approximation) [glmerMod]
# Family: binomial  ( logit )
# Formula: Matching ~ (WithinIU + WordPosition + WCount + (1 | Subject) +  
#                        (1 | StimID))
# Data: rememberdata
# 
# AIC      BIC   logLik deviance df.resid 
# 93389.0  93444.6 -46688.5  93377.0    77662 
# 
# Scaled residuals: 
#   Min      1Q  Median      3Q     Max 
# -6.1808 -0.8438  0.3058  0.8104  3.9358 
# 
# Random effects:
#   Groups  Name        Variance Std.Dev.
# Subject (Intercept) 0.08537  0.2922  
# StimID  (Intercept) 0.45884  0.6774  
# Number of obs: 77668, groups:  Subject, 101; StimID, 54
# 
# Fixed effects:
#   Estimate Std. Error z value Pr(>|z|)    
# (Intercept)   0.39181    0.16724    2.34   0.0191 *  
#   WithinIU      1.15867    0.02101   55.15   <2e-16 ***
#   WordPosition  0.34799    0.02635   13.21   <2e-16 ***
#   WCount       -0.03010    0.00359   -8.38   <2e-16 ***
#   ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Correlation of Fixed Effects:
#   (Intr) WthnIU WrdPst
# WithinIU    -0.082              
# WordPositin -0.061 -0.054       
# WCount      -0.804 -0.015 -0.015
plot(allEffects(glmm2))

#FORGOTTEN ONLY
forgottendata<-subset(WordPairs, MatchStatus!="bothremembered", select=c(Matching, MatchStatus, IUBoundary, WordPosition,WCount,Subject, StimID))
glmm3<-glmer(Matching ~ (IUBoundary + WordPosition + WCount + (1| Subject) + (1| StimID)), data= forgottendata, family = binomial)
summary(glmm3)
plot(allEffects(glmm3))
