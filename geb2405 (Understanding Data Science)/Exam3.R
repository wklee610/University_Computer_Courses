#Exercize 1 : 2 pts

library("gmodels")
library("ggplot2")

load("/Users/andy/Desktop/Final_term/geb/second_exam/Golf_2019_data_exam 2(1).RData")
#1.1 Reorder correctly the level of the variable diploma
#Pls input your code here

summary(Golf_2019$diploma)
Golf_2019$diploma <- factor(Golf_2019$diploma, levels=c("High school and below", "undergraduate", "postgraduate", "Technical or vocational college"))
summary(Golf_2019$diploma)

#1.2 Create a variable golf_score_cat where the categories will be 74 or below, 75 to 79, 80 to 84, 85 to 89, 90 or above
#Pls input your code here
table(Golf_2019$golf_score)
Golf_2019$golf_score_cat <- as.factor(Golf_2019$golf_score)
Golf_2019$golf_score_cat <- factor(Golf_2019$golf_score,
                                         levels=c("74 or below",
                                                  "75 to 79",
                                                  "80 to 84",
                                                  "85 to 89",
                                                  "90 or above"),
                                         ordered = TRUE)

summary(Golf_2019$golf_score_cat)
Golf_2019$golf_score_cat[Golf_2019$golf_score_cat<=74] <- "74 or below"
summary(Golf_2019$golf_score_cat)
#Exercise 2: 4pts
#2.1  Create a scatter plot showing the relation between age and income_per_month
ggplot(Golf_2019, aes(x=age, y=income_per_month)) + geom_point()

# 2.2 Form the plot created in 2.1, color the point according to the variable gender in the aes part
ggplot(Golf_2019, aes(color=gender, x=age, y=income_per_month)) + geom_point()

#2.3 Form the graph created in 2.2 add meaningful title and axis names
ggplot(Golf_2019, aes(color=gender, x=age, y=income_per_month)) + geom_point() + labs(title = "relationship between age and income per month", x="age", y="income per month")

#2.4 From the graph created in 2.3 add a line showing the correlation between age and income_per_month
ggplot(Golf_2019, aes(color=gender, x=age, y=income_per_month)) + geom_point() + labs(title = "relationship between age and income per month", x="age", y="income per month") + geom_smooth(method=loess)

#Exercise 3: 4pts
#3.1 Create a box plot of the variable golf_score by cga_certificate3cat
ggplot(Golf_2019, aes(x=golf_score, y=cga_certificate3cat)) + geom_boxplot()

#3.2 From the boxplot create in 3.1 edit title and axis name
ggplot(Golf_2019, aes(x=golf_score, y=cga_certificate3cat)) + geom_boxplot() +labs(title = "relationship between score and cga certificate", x="golf score", y="cga certificate")

#3.3 From the boxplot create in 3.2 what can you say about the median score of the golf for the different categories of trainers
80

# 3.3 From the boxplot create in 3.2 color the different boxplot with different colors
ggplot(Golf_2019, aes(x=golf_score, y=cga_certificate3cat)) + geom_boxplot() +labs(title = "relationship between score and cga certificate", x="golf score", y="cga certificate") + scale_fill_brewer(palette = "Blues")

#3.4 from the graph created in 3.3 remove the legend
ggplot(Golf_2019, aes(x=golf_score, y=cga_certificate3cat)) + geom_boxplot() +labs(title = "relationship between score and cga certificate", x="golf score", y="cga certificate") + scale_fill_brewer(palette = "Blues") + theme(axis.line = element_blank(), axis.title = element_blank(), axis.text = element_blank())

#Exercise 4: 7pts
#4.1 using CrossTable in gmodels package, produce a table of the variable golf_score_cat, showing the proportion of trainers in each category (or level)
#Pls input your code here
CrossTable(Golf_2019$golf_score_cat)
ScorePie <- data.frame(score=c("74 or below",
                               "75 to 79",
                               "80 to 84",
                               "85 to 89",
                               "90 or above"), n=c(5), p=c(0))
ggplot(ScorePie, aes(x="", y=p, fill=score)+geom_bar(stat="identity")+coord_polar("y",start=0) + geom_text()
       
#4.2 From the information in this table, prepare a dataframe named df that will help you to create a pie chart of golf_score_cat
#Pls input your code here
df <- data.frame(score=c("74 or below",
                         "75 to 79",
                         "80 to 84",
                         "85 to 89",
                         "90 or above"), n=c(), p=c())
#4.3 From df, Create a bar plot of the variable of interest
#Pls input your code here

ggplot(df,aes(x="",y=p, fill=score)) + geom_bar(stats = "identity")

#4.4 From the barplot in 4.3 create a pie chart
#Pls input your code here

#4.5 From the pie chart in 4.4 remove all the unnecessary elements
#Pls input your code here

#4.6 From the pie chart created in 4.5 add a title
#Pls input your code here

#4.7 from the pie chart in 4.6 add the percentage in each slice of th pie chart
#Pls input your code here


#exercise  5: 3pts
#5.1 Create a bar chart of making easy to compare the trainer's diploma and their professional certifcation (cgacertificate_3cat)
ggplot(Golf_2019, aes(x=diploma, fill=cga_certificate3cat)) + geom_bar()+facet_wrap(~cga_certificate3cat)
#5.2 Create a bar chart of making easy to compare the trainer's diploma and their professional certifcation (cgacertificate_3cat) depending on respondent gender
ggplot(Golf_2019, aes(x=diploma, fill=cga_certificate3cat)) + geom_bar()+facet_wrap(~gender)
# 5.3 edit the title and axis of the graph created in 5.3 and make sure that everything remain readable
ggplot(Golf_2019, aes(x=diploma, fill=cga_certificate3cat)) + geom_bar()+facet_wrap(~gender) + labs(title = "relationship between diploma and cga certificate", x="diploma", y="cga certificate")
