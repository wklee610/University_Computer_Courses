#Prepare the data

GSS_employment_status_simplified_V1<-GSS_employment_status_simplified_V1%>%mutate_if(is.character,as.factor)
GSS_employment_status_simplified_V1$sexnow<-na_if(GSS_employment_status_simplified_V1$sexnow,"NA")
GSS_employment_status_simplified_V1$sexnow<-na_if(GSS_employment_status_simplified_V1$sexnow,"No answer")
GSS_employment_status_simplified_V1$sexnow<-na_if(GSS_employment_status_simplified_V1$sexnow,"NA")
GSS_employment_status_simplified_V1$sexnow<-na_if(GSS_employment_status_simplified_V1$sexnow,"a gender not listed here")
GSS_employment_status_simplified_V1$sexnow<-na_if(GSS_employment_status_simplified_V1$sexnow,"transgender")
GSS_employment_status_simplified_V1$sexnow<-droplevels(GSS_employment_status_simplified_V1$sexnow)
GSS_employment_status_simplified_V1$padeg<-na_if(GSS_employment_status_simplified_V1$padeg,"NA")
GSS_employment_status_simplified_V1$padeg<-droplevels( GSS_employment_status_simplified_V1$padeg)
GSS_employment_status_simplified_V1$wrkstat_2<-GSS_employment_status_simplified_V1$wrkstat
GSS_employment_status_simplified_V1$wrkstat_2<-recode(GSS_employment_status_simplified_V1$wrkstat_2,"temp not working"="not working")
GSS_employment_status_simplified_V1$wrkstat_2<-recode(GSS_employment_status_simplified_V1$wrkstat_2,"unempl, laid off"="not working")
GSS_employment_status_simplified_V1$childs_2<-GSS_employment_status_simplified_V1$childs
GSS_employment_status_simplified_V1$childs_2<-cut(GSS_employment_status_simplified_V1$childs_2,breaks=c(-1,0,1,2,Inf))
GSS_employment_status_simplified_V1$childs_2<-recode(GSS_employment_status_simplified_V1$childs_2,"(-1,0]"="0","(0,1]"="1","(1,2]"="2","(2,Inf]"="3 or more")
GSS_employment_status_simplified_V1$age_sq<-GSS_employment_status_simplified_V1$age*GSS_employment_status_simplified_V1$age

#Prepare two reference levels full time and part-time
GSS_employment_status_simplified_V1$ref_level_full_time<-relevel(GSS_employment_status_simplified_V1$wrkstat_2,ref="working fulltime")
GSS_employment_status_simplified_V1$ref_level_part_time<-relevel(GSS_employment_status_simplified_V1$wrkstat_2,ref="working parttime")

#Prepare the models
Model_1<-multinom(data=GSS_employment_status_simplified_V1,GSS_employment_status_simplified_V1$ref_level_full_time~sexnow+age+degree)
stargazer(Model_1,type="text")

Model_2<-multinom(data=GSS_employment_status_simplified_V1,GSS_employment_status_simplified_V1$ref_level_full_time~sexnow+age+degree+race+childs_2)
stargazer(Model_2,type="text")

Model_3<-multinom(data=GSS_employment_status_simplified_V1,GSS_employment_status_simplified_V1$ref_level_full_time~sexnow+age+degree+race+childs_2+race:sexnow)
stargazer(Model_3,type="text")

#The two test below might need to creat a subset where there is no Na using na.omit since it works on other data
GSS_na_omit<-na.omit(GSS_employment_status_simplified_V1)
GSS_na_omit$ref_level_full_time<-relevel(GSS_na_omit$wrkstat_2,ref="working fulltime")
Model_1_bis<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_full_time~sexnow+age+degree)
stargazer(Model_1_bis,type="text")



#package generalhoslem #g should be larger than the number of predictors; df = g - 2
library(generalhoslem)
logitgof(GSS_na_omit$ref_level_full_time, fitted(Model_1_bis),g=10)
#no evidence of poor fit if p-value is up to 0.05 / it is the case here
library(DescTools)
PseudoR2(Model_1_bis,which="all")

# Anova test comparing the two models
Model_0 <- vglm(Ycateg ~ 1, family=multinomial(refLevel=1), data=dfMN)
anova(Model_0, Model_1, type="I")


#Classification matrice
library(summarytools)
ctable <- table(GSS_na_omit$ref_level_full_time,predict(Model_1_bis))
ctable <- table(GSS_na_omit$wrkstat_2,predict(Model_1_bis))

# Create the model_3_bis and compare its classification table to model_1_bis
Model_3_bis<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_full_time~sexnow+age+degree+race+childs_2+race:sexnow)
ctable3 <- table(GSS_na_omit$wrkstat_2,predict(Model_3_bis))

Model_2_bis<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_full_time~sexnow+age+degree+race+childs_2)
ctable2 <- table(GSS_na_omit$wrkstat_2,predict(Model_2_bis))

#Create new model 4, 5 and 6 which are the same with 1,2 and 3 but the reference level is part-time
GSS_na_omit$ref_level_part_time<-relevel(GSS_na_omit$wrkstat_2,ref="working parttime")
Model_4<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_part_time~sexnow+age+degree)
Model_5<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_part_time~sexnow+age+degree+race+childs_2)
Model_6<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_part_time~sexnow+age+degree+race+childs_2+race:sexnow)
table(GSS_na_omit$wrkstat_2,predict(Model_4))
table(GSS_na_omit$wrkstat_2,predict(Model_5))
table(GSS_na_omit$wrkstat_2,predict(Model_6))

Model_7<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_full_time~sexnow+age_sq+degree+race+childs_2)
table(GSS_na_omit$wrkstat_2,predict(Model_7))
stargazer(Model_7,type="text")

# Create model 8
GSS_na_omit$degree_reordered<-ordered(GSS_na_omit$degree,levels=c("lt high school","high school","junior college","bachelor","graduate"))
GSS_na_omit$race_reordered<-ordered(GSS_na_omit$race,levels=c("white","black","other"))
Model_8<-multinom(data=GSS_na_omit,GSS_na_omit$ref_level_full_time~sexnow+age_sq+degree_reordered+race_reordered+childs_2)
stargazer(Model_8,type="text")
table(GSS_na_omit$wrkstat_2,predict(Model_8))

#assumptions
# divide into binary regression and test the same assumptions as for logit
