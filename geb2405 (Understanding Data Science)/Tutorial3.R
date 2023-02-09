library('haven')
library('dplyr')
mcs <- read_dta("/Users/andy/Downloads/data\ for\ tut\ 3/2015\ Millennium\ Cohort\ Study/mcs.dta")

summary(mcs)

##Exercise 1##
#1
mcs$math <- as.factor(mcs$mths)
mcs$math <- recode(mcs$math, '1'='1. Strongly Disagree', '2'='2. Disagree',
                   '3'='3. Agree', '4'='4. Strongly Agree')
table(mcs$math)

#2
mcs$science <- as.factor(mcs$scien)
mcs$science <- recode(mcs$science, '1'='1. Strongly Disagree', '2'='2. Disagree',
                   '3'='3. Agree', '4'='4. Strongly Agree')
table(mcs$science)

#3
mcs$gender <- as.factor(mcs$sex)
mcs$gender <- recode(mcs$gender, '0'='0. Female', '1'='1. Male')
table(mcs$gender)

#4
mcs$bestsch <- as.factor(mcs$best)
mcs$bestsch <- recode(mcs$bestsch, '1'='1. Never', '2'='2. Sometimes', '3'='3. Most
                    Times', '4'='4. Always')



import("gfk_cleaed_eul")



#################Exercise 3 ####################

gfk_cleaed_eul <- read_dta('/Users/andy/Downloads/data\ for\ tut\ 3/gfk_cleaned_eul.dta')

gfk_cleaed_eul$education <- as.factor(gfk_cleaed_eul$educ)
gfk_cleaed_eul$education <- recode(gfk_cleaed_eul$education, "7" = "Did not complete GCSE/CSE/O-levels",
                                                             "6" = "Completed GCSE/CSE/O-levels",
                                                             "5" = "A-levels/Scottish Highers",
                                                             "4" = "I am still in education",
                                                             "3" = "Completed post-16 vocational course",
                                                             "2" = "Undergraduate degree",
                                                             "1" = "Postgraduate degree")
table(gfk_cleaed_eul$education)


#Lower working class = 7, Middle working class = 6, Upper working class = 5, 
#Lower middle class = 4, Middle middle class = 3, Upper middle class = 2, Upper class = 1

gfk_cleaed_eul$whichclass <- recode(gfk_cleaed_eul$whichclass, "7" = "Lower working class",
                                                               "6" = "Middle working class",
                                                               "5" = "Upper working class",
                                                               "4" = "Lower middle class",
                                                               "3" = "Middle middle class",
                                                               "2" = "Upper middle class",
                                                               "1" = "Upper class")
table(gfk_cleaed_eul$whichclass)


what is important is to make sur that you are using properly recode, cut, na_if and as.factor
