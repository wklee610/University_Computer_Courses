gfk_complete$age<-as.numeric(gfk_complete$age)
summary(gfk_complete$age)

#create a new subset of the variable
gfk_reduced<-subset(gfk_complete,select=c(hhincome,class,educ,sex,ethnic,mmetal,mclassic,age,vlocco, vloccopo,vmp,vukgof,vgla,vglapo, vna,vnapo, mobeasy))
gfk_reduced<-gfk_reduced%>%mutate_if(is.character,as.factor)
#vloco as numeric
gfk_reduced$vlocco_num<-as.numeric(gfk_reduced$vlocco)
table(gfk_reduced$vlocco_num,gfk_reduced$vlocco)
gfk_reduced$vlocco_num<-dplyr::recode(gfk_reduced$vlocco_num,'1'=0,'2'=1)
table(gfk_reduced$vlocco_num,gfk_reduced$vlocco)
#vloccopo as numeric
gfk_reduced$vloccopo_num<-as.numeric(gfk_reduced$vloccopo)
gfk_reduced$vloccopo_num<-dplyr::recode(gfk_reduced$vloccopo_num,'1'=0,'2'=1)
table(gfk_reduced$vloccopo_num,gfk_reduced$vloccopo)
#vmp as numeric
gfk_reduced$vmp_num<-as.numeric(gfk_reduced$vmp)
gfk_reduced$vmp_num<-dplyr::recode(gfk_reduced$vmp_num,'1'=0,'2'=1)
table(gfk_reduced$vmp_num,gfk_reduced$vmp)
#vukgof as numeric
gfk_reduced$vukgof_num<-as.numeric(gfk_reduced$vukgof)
gfk_reduced$vukgof_num<-dplyr::recode(gfk_reduced$vukgof_num,'1'=0,'2'=1)
table(gfk_reduced$vukgof_num,gfk_reduced$vukgof)
#vgla as numeric
gfk_reduced$vgla_num<-as.numeric(gfk_reduced$vgla)
gfk_reduced$vgla_num<-dplyr::recode(gfk_reduced$vgla_num,'1'=0,'2'=1)
table(gfk_reduced$vgla_num,gfk_reduced$vgla)
#vgla po asnumeric
gfk_reduced$vglapo_num<-as.numeric(gfk_reduced$vglapo)
gfk_reduced$vglapo_num<-dplyr::recode(gfk_reduced$vglapo_num,'1'=0,'2'=1)
table(gfk_reduced$vglapo_num,gfk_reduced$vglapo)
#vna as numeric
gfk_reduced$vna_num<-as.numeric(gfk_reduced$vna)
gfk_reduced$vna_num<-dplyr::recode(gfk_reduced$vna_num,'1'=0,'2'=1)
table(gfk_reduced$vna_num,gfk_reduced$vna)
#vnapo as numeric
gfk_reduced$vnapo_num<-as.numeric(gfk_reduced$vnapo)
gfk_reduced$vnapo_num<-dplyr::recode(gfk_reduced$vnapo_num,'1'=0,'2'=1)
table(gfk_reduced$vnapo_num,gfk_reduced$vnapo)
# create the score variable
gfk_reduced$political_cap<-gfk_reduced$vnapo_num+gfk_reduced$vna_num+gfk_reduced$vglapo_num+gfk_reduced$vgla_num+gfk_reduced$vukgof_num+gfk_reduced$vmp_num+gfk_reduced$vloccopo_num+gfk_reduced$vlocco_num
summary(gfk_reduced$political_cap)
describe(gfk_reduced$political_cap)
#create the variable generation
gfk_reduced$year_birth_cat<-2014-gfk_reduced$age
gfk_reduced$year_birth_cat<-cut(gfk_reduced$year_birth_cat,breaks = c(1920,1945,1964,1984,1996,2000))
table(gfk_reduced$year_birth_cat)
gfk_reduced$year_birth_cat<-recode(gfk_reduced$year_birth_cat,"(1920,1945]"="Born before 1945","(1945,1964]"="Boomers","(1964,1984]"="Generation X","(1984,1996]"="Millenium","(1996,2000]"="Generation Z")
table(gfk_reduced$year_birth_cat)
#create ethnic_3cat
gfk_reduced$ethnic_2cat<-gfk_reduced$ethnic
table(gfk_reduced$ethnic_2cat)
gfk_reduced$ethnic_2cat<-recode(gfk_reduced$ethnic_2cat, "Asian/Asian British - Indian, Pakistani, Bangladeshi, Other"="Other","Chinese/Chinese British"="Other","Middle Eastern/Middle Eastern British - Arab, Turkish, other"="Other","Mixed race - other"="Other","Mixed race - White and Black/Black British"="Other","Other ethnic group"="Other", "Rather not say"="Other","Black/Black British - Caribbean, African, other"="Other")
table(gfk_reduced$ethnic_2cat)

gfk_cleaned<-filter(gfk_reduced,!educ=="4. Still in ed")

##mmetal_3
gfk_cleaned$mmetal_3<-gfk_cleaned$mmetal
table(gfk_cleaned$mmetal)
gfk_cleaned$mmetal_3<-recode(gfk_cleaned$mmetal_3,"Dislike"="Dislike or dislike a lot","Dislike a lot"="Dislike or dislike a lot","Like a lot"="Like or like a lot","Like"="Like or like a lot")
table(gfk_cleaned$mmetal_3)
##mclassic
gfk_cleaned$mclassic_3<-gfk_cleaned$mclassic
table(gfk_cleaned$mclassic_3)
gfk_cleaned$mclassic_3<-recode(gfk_cleaned$mclassic_3,"Dislike"="Dislike or dislike a lot","Dislike a lot"="Dislike or dislike a lot","Like a lot"="Like or like a lot","Like"="Like or like a lot")
table(gfk_cleaned$mclassic_3)

# droplevel educ
gfk_cleaned$educ<-droplevels(gfk_cleaned$educ)

# create hhincome_cat5

gfk_cleaned$hhincome_cat<-recode(gfk_cleaned$hhincome,"Under ?5,000"="under 10 000", "?5,000 - ?10,000"="under 10 000","?10,000 - ?14,999"="10 000 to 20 000","?15,000 - ?19,999"="10 000 to 20 000","?20,000 - ?24,999"="20 000 to 30 000","?25,000 - ?29,999"="20 000 to 30 000")
gfk_cleaned$hhincome_cat<-recode(gfk_cleaned$hhincome_cat,"?30,000 - ?34,999"="30 000 to 40 000","?35,000 - ?39,999"="30 000 to 40 000","?40,000 - ?44,999"="40 000 to 50 000","?45,000 - ?49,999"="40 000 to 50 000")
gfk_cleaned$hhincome_cat<-recode(gfk_cleaned$hhincome_cat,"?50,000 - ?54,999"="50 000 and above","?55,000 - ?59,999"="50 000 and above","?60,000 - ?64,999"="50 000 and above","?65,000 - ?69,999"="50 000 and above","?70,000 - ?74,999"="50 000 and above","?75,000 - ?79,999"="50 000 and above","?80,000 - ?84,999"="50 000 and above","?85,000 - ?89,999"="50 000 and above","?90,000 - ?94,999"="50 000 and above","?95,000 - ?99,999"="50 000 and above","?100,000 - ?149,999"="50 000 and above","?150,000 - ?199,999"="50 000 and above","Over ?200,000"="50 000 and above")
gfk_cleaned$hhincome_cat<-na_if(gfk_cleaned$hhincome_cat,"Refused")
gfk_cleaned$hhincome_cat<-droplevels(gfk_cleaned$hhincome_cat)
gfk_cleaned$hhincome_cat<-ordered(gfk_cleaned$hhincome_cat,levels=c("under 10 000","10 000 to 20 000","20 000 to 30 000","30 000 to 40 000","40 000 to 50 000","50 000 and above"))
table(gfk_cleaned$hhincome_cat)

#set up reference level
gfk_cleaned$mmetal_ref_neither<-relevel(gfk_cleaned$mmetal_3,ref="Neither like nor dislike")
#creat the three levels Bourdieu, Weber, Friedman
mmetal_model_bourdieu1<-multinom(data=gfk_cleaned,gfk_cleaned$mmetal_ref_neither~hhincome_cat+educ+political_cap)
stargazer(mmetal_model_bourdieu1,type="text")
mmetal_model_weber1<-multinom(data=gfk_cleaned,gfk_cleaned$mmetal_ref_neither~sex+class+ethnic_2cat+political_cap)
stargazer(mmetal_model_weber1,type="text")
mmetal_model_friedman1<-multinom(data=gfk_cleaned,gfk_cleaned$mmetal_ref_neither~sex+class+ethnic_2cat+year_birth_cat+political_cap)
stargazer(mmetal_model_friedman1,type="text")

#Test the predictive value and the goodness of the model
gfk_cleaned_na_omit<-na.omit(gfk_cleaned)
gfk_cleaned_na_omit$mmetal_ref_neither<-relevel(gfk_cleaned_na_omit$mmetal_3,ref="Neither like nor dislike")
mmetal_model_friedman2<-multinom(data=gfk_cleaned_na_omit,gfk_cleaned_na_omit$mmetal_ref_neither~sex+class+ethnic_2cat+year_birth_cat+political_cap)
stargazer(mmetal_model_friedman2,type="text")

#package generalhoslem #g should be larger than the number of predictors; df = g - 2
library(generalhoslem)
logitgof(gfk_cleaned_na_omit$mmetal_ref_neither, fitted(mmetal_model_friedman2),g=20)
#no evidence of poor fit if p-value is up to 0.05 / it is the case here
library(DescTools)
PseudoR2(mmetal_model_friedman2,which="all")
#confusion matrice
ctable2 <- table(gfk_cleaned_na_omit$mmetal_3,predict(mmetal_model_friedman2))

