library(gmodels)
library(sjstats)
library(sjPlot)
library(GDAtools)
library(LogisticDx)
library(jtools)
library(regclass)
library(DescTools)
library(dplyr)
library(tidyverse)
library(gtools)
library(huxtable)
library(car)


load("/Users/andy/Desktop/Final_term/geb/week11/heart data R file(1).RData")
CrossTable(heart.data$target, heart.data$sex)

#Exercise 1: Exploring the data
#1.	Using the sjt.xtab function produce a contingency table of the variable cp (fro chest pain) and sex, showing the column and row percentage
sjt.xtab(heart.data$cp,
         heart.data$sex,
         show.exp = TRUE,
         show.row.prc = TRUE,
         show.col.prc = TRUE)

#2.	Among the people suffering from Typical Angina, what is the proportion of female.
CrossTable(heart.data$sex, heart.data$cp)
#18/50 = 36% 


#3.	Explain wether the chi-square test is significant or not (at 90% interval of confidence) and comment the cramer's V value.
crosstable_statistics(heart.data, x1 = cp, x2 = sex, statistics = c("cramer"))
#Cramer's V = 0.1501
#chi-squared distribution should have confidence at 95% interval of confidence, so it is not significant

#4.	From the result of the local pem, can we say that female are less likely to be asymptomatic?
pem(heart.data$sex,
    heart.data$cp)
#yes

#5.	From the result of the local pem, can we say that male more likely to suffer from non angina pain?
pem(heart.data$sex,
    heart.data$cp)
#yes


#Exercise 2: building and comparing models

#6.	Create a first model titled heart_D_1 which predict whether people are suffering or not from heart disease and which includes age, sex, cp (for chest pain), thalach (for maximum heart rate achieved), ca (number of major vessels).
myData <- heart.data
heart_D_1 <- glm(target~age+sex+cp+thalach+ca, family="binomial", data = myData)

#7.	Create a second model heart_D_2 which predict whether people are suffering or not from heart disease and which includes age, sex, cp (for chest pain), thalach (for maximum heart rate achieved), ca (number of major vessels), slope and oldpeak
heart_D_2 <- glm(target~age+sex+cp+thalach+ca+slope+oldpeak, family="binomial", data = myData)

#8.Using exports_summs print the results and compare the different models (AIC/BIC)
export_summs(heart_D_1, heart_D_2)

#MODEL                    heart_D_1             heart_D_2
#AIC                        272.79                257.26
#BIC                        302.50                294.39


#9.	For the two model produce a confusion matrix and report the Mac Fadden R2
confusion_matrix(heart_D_1)
confusion_matrix(heart_D_2)

PseudoR2(heart_D_1)
#McFadden  0.3851292
PseudoR2(heart_D_2)
#McFadden  0.4319106


#10.	Complete this sentence:
#According to model heart_D_2, when we move form male to female the chance at the odd to suffer heart disease ..... by..... %
summary(heart_D_2)
#by the odd, 80.46726%

#11.	Complete this sentence:
#According to model heart_D_2, for each additional  major vessel (variable ca) the chance to suffer heart disease by ...%  at the odd.
summary(heart_D_2)
#49.51455%

#Exercise 2:
#12.	For model heart_D_2, since thalach (for maximum heart rate achieved) seems to play an important role verify that thalach does not violate the assumption of linearity at the log odd.
heart_D2_add<-glm(target~sex+cp+thalach:age+ca+slope+oldpeak, family="binomial", data = myData)
summary(heart_D2_add)
#after see Pr(|z|), there are no issue.

#13.	For model heart_D_2 since thalach (for maximum heart rate achieved) might varied with sex, test a possible interaction between those two variables (assumption of additivity)
heart_D2_add<-glm(target~sex+cp+thalach:sex+ca+slope+oldpeak, family="binomial", data = myData)
summary(heart_D2_add)
#after see Pr(|z|), there are no issue.
  
#14.	Using the vif function check the collinearity in the models heart_D_2
vif(heart_D_2)
#ALL of GVIF^(1/2*Df)) values are below of 2, so there aren't any issues

# 15.	In the models heart_D_2, do you have any influential cases?
dx(heart_D_2)
plot(heart_D_2)
#There are cases of outliers, but not yet a way to know there are influential cases.