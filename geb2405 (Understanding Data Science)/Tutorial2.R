#to be loaded
library(forcats)
library(psych)

#exercize 1
#Load the datset USArrests
data("USArrests")
head(USArrests)
#Find the following mean, median and sd
#By applying the command summary to the entire dataset, you can get the median and mean for every continuous variable
summary(USArrests)
#Then for each variable of interest you can get the SD using the command SD
sd(USArrests$Murder)
sd(USArrests$Assault)
sd(USArrests$UrbanPop)
#When you use describe (psych package) you can get immediatly the mean, the median and the SD
describe(USArrests$Murder)

#Exercize 2
#Load the UCBA ADmission
data("UCBAdmissions")
head(UCBAdmissions)
#When you use different command only summary and str works
summary(UCBAdmissions)
describe(UCBAdmissions)
table(UCBAdmissions)
str(UCBAdmissions)
# This can from the fact that UCBA Admission is not a "common data frame", as you can see after running the command head, it contains several tables

#Exercise 3
#Load the gss_cat data from R
library(forcats)
data("gss_cat")
head(gss_cat)
#use str for the command rincome and then levels
str(gss_cat$rincome)
levels(gss_cat$rincome)
#From this you can see rincome is organised in a decreasing order but the levels No answer, Don't know, refused and Not applicable can all put at the end
#Besides, for future analysis you will need to group No answer, Don't know, refused and Not applicable into NA (otherwise you analylitcal models can be biased)
table(gss_cat$marital)
# from table I can see 1807 widowed and 3383 divorced
table(gss_cat$relig)
147/21483*100
#From the nevironment I can see that I have 21483 respondents. Therfore the proportion of buddhist is 147/21483*100=0.7%
levels(gss_cat$relig)
#the ninth level is Hinduism

#Exercise 4
str(CGA_golf_train_short)
#while using str, you can first identify the factor variables for which an order is needed to make the correlation meaningfull
levels(CGA_golf_train_short$diploma)
#the you explore the different categorical variables which need to be order in a hierarchical order
levels(CGA_golf_train_short$Golf_trainer_category)
levels(CGA_golf_train_short$Handicap)
levels(CGA_golf_train_short$Annual_course_frequentation)
levels(CGA_golf_train_short$annual_earning)
levels(CGA_golf_train_short$Training_earning_ratio)
levels(CGA_golf_train_short$Satisfaction_with_earning)
summary(CGA_golf_train_short$Year_birth)
#the minimum is -1 therefore at least one value will need recoding
#When looking at the dataset and organising the data depending of Year of birth the older trainer is  born in 1950, which seems plausible
str(CGA_golf_train_short)
#str display the 30 variables, so we can see that two of them are character which is noted chr  
#after looking at the results of str, I can see many variable have only two levels anb those levels are not missing or missing value
#therefore I just need to inspect, work_place_cat , diploma, past_practice,Golf_trainer_category, PGA_other_country_certification, Handicap, Annual_course_frequentation, annual_earning, Training_earning_ratio, Staisfaction with earning, social insurance, and workplace
levels(CGA_golf_train_short$Golf_trainer_category)
levels(CGA_golf_train_short$Handicap)
levels(CGA_golf_train_short$Annual_course_frequentation)
levels(CGA_golf_train_short$annual_earning)
levels(CGA_golf_train_short$Training_earning_ratio)
levels(CGA_golf_train_short$Satisfaction_with_earning)
levels(CGA_golf_train_short$work_place_cat)
levels(CGA_golf_train_short$workplace)
levels(CGA_golf_train_short$social_insurance)
levels(CGA_golf_train_short$Training_earning_ratio)
levels(CGA_golf_train_short$Year_experience_as_trainer)
levels(CGA_golf_train_short$year_last_golf_qualification)
levels(CGA_golf_train_short$Past_practice)
levels(CGA_golf_train_short$PGA_other_country_certification)
#Therefore I can see that the following variable have "missing value" which must be recoded as Na in R
#year_last_golf_qualification
#Golf_trainer_category
#PGA_other_country_certification







arg = [test.c, 2, 3]

for(i = 0; i < argv - 1; i++){
    arg[i] = argv[i+1]
}


arg[0] = argv[1]
arg[1] = argv[2]
arg[2] = argv[3]


[]
args = [test.c, 2, 3]
null = 아무의미 없음.


x = 1 + 3

arg[i] = argv[i+1]


arg[0] = argv[1]

argv = [normal]
arg = []

[c]  -->  [ a, , ]


