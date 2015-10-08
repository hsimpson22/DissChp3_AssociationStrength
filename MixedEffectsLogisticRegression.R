rm(list=ls(all=TRUE)) #
library(lmerTest)
library(effects)
WordPairs<-read.table(file = "/Users/heathersimpson/Documents/Dissertation/Articles/Chp3_MutualInfoIUboundaries/WordPairsScores.csv", sep="\t", quote = "", header = TRUE, comment.char="")
str(WordPairs)
WordPairs$WithinIU[WordPairs$WithinIU==0]<-"no"
WordPairs$WithinIU[WordPairs$WithinIU==1]<-"yes"
WordPairs$WithinIU<-as.factor(WordPairs$WithinIU)
#Generalized Linear Mixed Model (binomial) on Matching = 0/1
glmm<-glmer(Matching ~ (WithinIU + WordPosition + WCount + (1| Subject) + (1| StimID)), data= WordPairs, family = binomial)
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


#But high volume of both forgotten datapoints within IU are inflating this effect, and they may indicate salience of words at IU boundaries as opposed to within IUs, rather than the unithood of IU representation. So will try again with only the remembered vs. non-matching

#subset the data for those two things
rememberdata<-subset(WordPairs, MatchStatus!="bothforgotten", select=c(Matching, MatchStatus, WithinIU, WordPosition,WCount,Subject, StimID))
glmm2<-glmer(Matching ~ (WithinIU + WordPosition + WCount + (1| Subject) + (1| StimID)), data= rememberdata, family = binomial)
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
