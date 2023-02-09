#Packages to load
library(LogisticDx)
library(jtools)
library(regclass)
library(DescTools)

#Import the data on student's admission in graduate school
mydata <- read.csv("https://stats.idre.ucla.edu/stat/data/binary.csv")

#Modeling students admissions, with undergraduate university rank as independent variable
mylogitcategorical <- glm(admit ~ rank, data = mydata, family = "binomial")

#data preparation
CGA_golf_train_short$Handicap_5cat<- CGA_golf_train_short$Handicap
CGA_golf_train_short$Handicap_5cat<-recode(CGA_golf_train_short$Handicap_5cat,"0 to 4"="4 and below")
CGA_golf_train_short$Handicap_5cat<-recode(CGA_golf_train_short$Handicap_5cat,"below 0"="4 and below")
CGA_golf_train_short$Handicap_5cat<-recode(CGA_golf_train_short$Handicap_5cat,"up to 20"="20 or ab/don't have")
CGA_golf_train_short$Handicap_5cat<-recode(CGA_golf_train_short$Handicap_5cat,"Don't have"="20 or ab/don't have")
CGA_golf_train_short$Handicap_5cat<-factor(CGA_golf_train_short$Handicap_5cat,levels=c("4 and below", "4 to 9","9 to 16","16 to 20", "20 or ab/don't have"))


#Let's practice 1 : building model
logitman1<-glm(Golf_club_manager~Handicap_5cat+Year_experience_as_trainer+Sex,data=CGA_golf_train_short,family="binomial")
logitman2<-glm(Golf_club_manager~Handicap_5cat+Year_experience_as_trainer+Sex+diploma,data=CGA_golf_train_short,family="binomial" )
logitman3<-glm(Golf_club_manager~Handicap_5cat+Year_experience_as_trainer+Sex+diploma+Past_practice,data=CGA_golf_train_short,family="binomial" )
summary(logitman1)
summary(logitman2)
summary(logitman3)


#Let's practice 3: Goodness and fit of the three models the ROC curve
gof(logitman1)
gof(logitman2)
gof(logitman3)


#Assessing the fitness using Mac Fadden R2
#Package DescTools
PseudoR2(logitman1)
PseudoR2(logitman1,which="all")
PseudoR2(logitman2)
PseudoR2(logitman2,which="all")
PseudoR2(logitman3)
PseudoR2(logitman3,which="all")

#Assessing the strength using a confusion Matrix
#Package regclass
confusion_matrix(logitman1)
confusion_matrix(logitman2)
confusion_matrix(logitman3)


#demonstration export_summs in jtools package
export_summs(logitman1,logitman2,logitman3,scale=TRUE)
