#Exam 1

load("/Users/andy/Desktop/Exam - 1 - Data.RData")

# 1 pt. Merge together in a new data frame named GE2405_survey_all the information contained in GEB2405_Survey_1to25 and GEB2405_Survey_26to50
#Pls input your code below
GE2405_survey_all <- rbind(GEB2405_Survey_1to25, GEB2405_Survey_26to50)
View(GE2405_survey_all)

# 1pt. How many characters variable do you have in the GE2405_survey_all
#Pls input your code below and write a sentence
describe(GE2405_survey_all)

# 2pt Transform the variables time_online1,rework_tut1, work_online_3, rework_tut3 as factor variable
#Pls input your code below
GE2405_survey_all$time_online1 <- as.factor(GE2405_survey_all$time_online1)
GE2405_survey_all$rework_tut1 <- as.factor(GE2405_survey_all$rework_tut1)
GE2405_survey_all$work_online_3 <- as.factor(GE2405_survey_all$work_online_3)
GE2405_survey_all$rework_tut3 <- as.factor(GE2405_survey_all$rework_tut3)

# 1pt. What is the proportion of Year4 students in the class
#Pls input your code below
GE2405_survey_all$Year_study <- as.factor(GE2405_survey_all$Year_study)
summary(GE2405_survey_all)

#Pls write a sentence for the answer

# 1pt. How many students spent 1 hour or more  to rework on tutorial 1
#Pls input your code below
summary(GE2405_survey_all$rework_tut1)

#Pls write a sentence for the answer

# 1pt. What is the third levels of the variable rework_tut3
#Pls input your code below
summary(GE2405_survey_all$rework_tut3)

#Pls write a sentence for the answer

#1pt. For the variable school, recode the level Data Science SDsc
#Pls input your code below
GE2405_survey_all$school <- recode(GE2405_survey_all$school, "Data Science"="SDsc")

# 1pt. Do the variables time_online1,rework_tut1 need to be modify? why?
#Pls input your code below
summary(GE2405_survey_all$time_online1)
summary(GE2405_survey_all$rework_tut1)
summary(GE2405_survey_all$work_online_3)

#Pls write a sentence for the answer

# 2pt.Pls proceed to the modifications you identified in the previous question
#Pls input your code below
GE2405_survey_all$time_online1 <- as.factor(GE2405_survey_all$time_online1)
GE2405_survey_all$rework_tut1 <- as.factor(GE2405_survey_all$rework_tut1)
#summary(GE2405_survey_all$time_online1)
GE2405_survey_all$time_online1 <- factor(GE2405_survey_all$time_online1,
                                         levels=c("I spent 30 minutes or less",
                                                  "I spend 30 to 45 minutes",
                                                  "I spent 45 minutes to 1 hour",
                                                  "I did not work on this online video",
                                                  "I spent more than 1 hour"),
                                         ordered = TRUE)


# 2pt. Analyse the variable completed_GE and indicate the levels that need to be recoded
#Pls input your code below
GE2405_survey_all$completed_GE <- as.factor(GE2405_survey_all$completed_GE)
summary(GE2405_survey_all$completed_GE)


#Pls write a sentence for the answer


# 1pt. Knowing that BB indicates that only 34% of the students downloaded the extra homework documents, do you think that students exaggerate their commitment to optional homework
#Pls input your code below
summary(as.factor(GE2405_survey_all$homework_tut2))
19/50 * 100

#Pls write a sentence for the answer

# 1pt. What is the mean, the median and the standard deviation of the variable current_GPA
#Pls input your code below
mean(GE2405_survey_all$current_GPA)
median(GE2405_survey_all$current_GPA)
sd(GE2405_survey_all$current_GPA)


#Pls write a sentence for the answer


# 1pt. What is the mean, the median and the standard deviation of the variable expected_GPA
#Pls input your code below
mean(GE2405_survey_all$expected_GPA)
median(GE2405_survey_all$expected_GPA)
sd(GE2405_survey_all$expected_GPA)

#Pls write a sentence for the answer


# 1pt. Create a variable GPA_dif showing the difference between expect and current GPA
#Pls input your code below
GE2405_survey_all$GPA_dif <- GE2405_survey_all$expected_GPA - GE2405_survey_all$current_GPA

# 1pt. From GPA_dif create a categorical variable named GPA_dif_cat showing whether students are expecting "no improvement", "little improvment", "huge improvement.
#For this question we will consider that little improvement is an improvement below 0.1, and huge improvement up to 0.1
#Pls input your code below
GE2405_survey_all$GPA_dif_cat <- "no improvement"
GE2405_survey_all$GPA_dif_cat[GE2405_survey_all$GPA_dif > 0] <- "little improvement"
GE2405_survey_all$GPA_dif_cat[GE2405_survey_all$GPA_dif >= 0.1] <- "huge improvement"

# 1pt. Rename the levels of GPA_dif_cat as follow "no improvement expected", "little improvement expected,"huge improvement expected"
#Pls input your code below
GE2405_survey_all$GPA_dif_cat <- recode(GE2405_survey_all$GPA_dif_cat,
                                        "no improvement" = "no improvement expected",
                                        "little improvement" = "little improvement expected",
                                        "huge improvement" = "huge improvement expected")

# 1pt. For the variable gender transform the level "Other" as an non-answer (this is just for testing your capacity to use the appropriate command, doesn't mean that other is not a valid/acceptable answer)
#Pls input your code below
GE2405_survey_all$gender <- recode(GE2405_survey_all$gender,
                                   "Other" = "non-answer")

