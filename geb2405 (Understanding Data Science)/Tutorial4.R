#SCrip for tutorial 4

#Exercise 1: See excel for 1.1
#Important remark regarding the codebook created with excel
#For question one: multiple choices are possible, so the questions is splited into several binary variables (Yes/No)
#For the question where di you buy your last cup of coffee, the respondent were supposed to select only one choice.
#Therefore for the questionnaires where the respondent select two categories, we will consider it as an non-answer.


#1.2 Importing the excel with the first respondent answwer
#Be carefull if you just import the first raw with your variable name R will not know what kind of variables you have.
#Therefore, the data will all be NAs after edition with the fix command. 

#Exercise 2
#use the fix command to edit the data
#fix(name of the data.frame)
fix(coffee_basic)
#once you edit the data creat a new dataset from coffee_1to10=coffee_basic
#Re-do the same thing with respondent 11 to 20
#Merge the existing data
coffee_all=rbind(coffee_1to10,coffee_11to20)

#Exercise 3
#Create the new factor variable and edit their label

#Option for beginner (what you are supposed to be in this class)
#You do it one by one (I just provide some example here)
coffee_all$gender_fac=as.factor(coffee_all$gender)
coffee_all$gender_fac=recode(coffee_all$gender_fac,"0"="No","1"="Yes")

coffee_all$cappucino_fac=as.factor(coffee_all$cappucino)
coffee_all$cappucino_fac=recode(coffee_all$cappucino_fac,"0"="No","1"="Yes")

#Create a score variable with the total number of afferent coffee drunk by each respondent
coffee_all$coffee_score=coffee_all$cappucino+coffee_all$latte+coffee_all$americano+coffee_all$expresso+coffee_all$double_expresso

#Create a new variable with all the possible combination of coffee
coffee_all$coffee_combin=paste(coffee_all$cappucino,coffee_all$latte,coffee_all$americano,coffee_all$expresso,coffee_all$double_expresso)
table(coffee_all$coffee_combin)
coffee_all$coffee_combin=recode(coffee_all$coffee_combin,"0 0 0 1 0"="Expresso only","0 0 0 1 1"="Expresso and double expresso","0 0 1 0 0"="Americano only","0 0 1 1 0"="americano and expresso","0 1 0 0 0"="latte only","0 1 1 0 0"="latte and americano","1 0 0 0 0"="capuccino only","1 1 0 0 0"="cappucino and latte","1 1 1 0 0"="capuccino latte and americano")


#This part of my script is not for beginner but can help you in the future or if you are already familiar with R

#Option for advanced users. Just keep it in your computer if you want to improve in the future
#will not be necessary for this exam

#First advance option to transfrom as the chracter variable as factor
#You can transfrom all the character variable using a pipe and the following line of code
#The only issue is that your initial data will be modified
coffee_all=coffee_all%>%mutate_if(is.character,as.factor)

# Second advance option to create new factor variables and then add them to the initial dataframe with modifying the raw data
#It requires three steps
#creating a new dataframe where the selected variable a transformed into factor variables
#variable to transform are selected with select
#mutate is used to mutate
#across (here I put 1:8 because I mutate the variables 1 to 8)
#as.factor transform into factor
coffee_all2=coffee_all %>%select(cappucino, americano, expresso,double_expresso,pur_place,univ_dep,stud_level,gender) %>% mutate(across(1:8, as.factor))
#rename the variables created in the former dataframe using a single line of code
# use the command rename_with
#.fn=~paste0(.,"fac") means add at the end of each column name in the dataframe coffee_all2 the letter "fac". 
coffee_all2=rename_with(coffee_all2, .fn = ~paste0(., "fac"))
#add the newly created column in with the initial data and the new one into a new dataset
coffe3=cbind(coffee_all,coffee_all2)
#Important notice
#AS you can see the advantage of creating new variable in a single code or one by one depends on the number of variables you need to create

#Recoding using advanced techniques, to apply a same recoding to different variables
#EXample, recode all the 0=No and 1=Yes for the different kind of coffee with one single line of code
coffee_all2=coffee_all2%>%mutate_at(c("cappucinofac","americanofac", "expressofac","double_expressofac"),~recode(.,"1"="Yes","0"="No"))
