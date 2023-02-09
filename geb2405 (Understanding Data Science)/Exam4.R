library(gmodels)
library(sjstats)
library(sjPlot)
library(GDAtools)
library(stats)
library(LogisticDx)
library(regclass)
library(DescTools)
library(jtools)
library(dplyr)
library(car)
library(tidyverse)
library(ggplot2)
library(ggrepel)
library(gtools)
library(huxtable)
library(sjPlot)
library(generalhoslem)
library(summarytools)
library(nnet)
library(stargazer)

load("/Users/andy/Desktop/Final_term/geb/final/Final exam_data.RData")

#Data preparation:
#Transform the variable vote as factor in both urban and rural subset
urban_subset$Vote <- as.factor(urban_subset$Vote)
rural_subset$Vote <- as.factor(rural_subset$Vote)

#Section 1:Binary regression
#Question 1
#Using the sjt.xtab function produce a contingency table of the variable showing the relation between Vote and Gender in the rural subset
sjPlot::sjt.xtab(rural_subset$Vote,
                 rural_subset$Gender,
                 show.exp = TRUE,
                 show.row.prc = TRUE,
                 show.col.prc = TRUE)

#Question 2:
#Report and analyse the chi-square p-value and the Cramer's V
CrossTable(rural_subset$Vote,
           rural_subset$Gender,
           chisq = TRUE)
#Chi^2 =  53.98032
#p =  2.025076e-13

crosstable_statistics(rural_subset,
                      x1 = Vote,
                      x2 = Gender,
                      statistics = c("cramer"))
#Chi-squared: 53.6100 
#p-value: < .001***
#Cramer's V: 0.0924


#Question 3
#After anaylising the variable Vote in the rural subset, indicate the maximum nbr of EPV that you can include in your future model
model0 <- glm(formula = Vote ~ Gender,
              family = "binomial",
              data = rural_subset)
#Maximum of 5~10 should indicate


#Question 4
#built a first model predicting the Vote in rural subset. 
#You must include Gender, Party, diploma, Fam_income, age and House_owned as predictor
model1 <- glm(formula = Vote ~ Gender + Party + diploma + Fam_income + age + house_owned,
              family = "binomial",
              data = rural_subset)



#Question 5
#Does the variable age violate the assumption of linearity at the log odd (precise provide the code and a written answer)
model1 <- glm(formula = Vote ~ Gender + Party + diploma + Fam_income + age + house_owned,
              family = "binomial",
              data = rural_subset)
#yes


#Question 6:
#Verify that there is no serious collinearity issue (precise provide the code and a written answer)

#when formula is higher than 2 (formula > 2) will indicate an issue



#Question 7:
#built a second model predicting the vote in rural subset
#You must include Gender, Party, diploma, Fam_income, age, Union Member and House_owned as predictor
model2 <- glm(formula = Vote ~ Gender + Party + diploma + Fam_income + age + Union_member + house_owned,
              family = "binomial",
              data = rural_subset)


#Question 8:
#By comparing the two models AIC, can it be said that model2 is better than model1 (pls justify your answer)
export_summs(model1, model2, scale = TRUE)

#AIC = 7414.91 / 7332.57
#Model 2 has lower AIC which shows that it is a better model



#Question 9:
#Complete the sentence (while showing the detail of your calculation)
#According to model 2, when we move from female to male the chance at the odd to vote, increase by .....%
exp(0.23)
#125.86%


#Question 10
#Complete the sentence (while showing the detail of your calculation)
#According to model 2, when we move from Party member to Non party member the chance at the odd to vote, decrease by .....%
exp(-0.89)
100 - 41.06558
#58.93442%

#Question 11
#In model2, do we have any influential point (provide the code and a written answer)
logitman <- model2
model3 <- predict(logitman, type="response")


#Question 12
#In model2, do we have any additivity between Party and Gender
summary(model2)



#Question 13
#Make a confusion matrix of model 2 and comment it.
confusion_matrix(model2)
#Either false positives, negatives have high percentage

#Question 14
#Retrive the Mac Fadden R2 of model2 and comment it
PseudoR2(model2)
#MacFadden 0.07101596



#Section 2 :multinomial logistic regression
#Question 15
#In the urban_subset, for the variable Happiness_cat set up Average Happiness as reference level
urban_subset$Happiness_cat <- relevel(urban_subset$Happiness_cat, ref = "Average Happiness")

#Question 16
#In the CGSS_Reduce_exam4_cleanded data,Built a model_3 predicting Happiness_cat, with Gender,diploma,House_owned_stat,Ethnicity,log_age,Hukou as predictor
model_3 <- multinom(data = CGSS_Reduce_exam4_cleanded,
                    CGSS_Reduce_exam4_cleanded$Happiness_cat ~ Gender + diploma + House_owned_stat + Ethnicity + log_age + Hukou)


#Question 17
#Answer the following question according to model 3
# When we move from female to male, the chance at the odd to report high happiness decrease by    %.
stargazer(model_3, type = "text")
exp(-0.151)
1 - 0.8598477
#0.14015%

#When we move from rural to urban hukou, the chance at the odd to report high happiness increase by    %.
exp(0.423)
#152.6534%

#Question 18
#Report the mac fadden of model 3 (don't worry if any error messgae, this is just an exercise)
PseudoR2(model_3, which = "all")

#Question 19
#Built the same model as model3 with the urban_subset_reduced and print a confusion matrix of this model (you must not include hukou in this model)
model_3add <- multinom(data = urban_subset_reduced,
                       urban_subset_reduced$Happiness_cat ~ Gender + diploma + House_owned_stat + Ethnicity + log_age)

model_3add_na_omit <- na.omit(model_3add)
confusion_matrix(model_3add_na_omit,
                 predict(model_3add))

                 