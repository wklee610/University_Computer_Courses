library(ggplot2)
library(forcats)

load("/Users/andy/Desktop/Final_term/geb/week 6/tu 1 -exam -data.RData")

#Question 1
#create an histogram of HDI (HDI means Human Development Index)
ggplot(hdro, aes(x = HDI)) + geom_histogram()

#Question 2
#From the histogram created in question 1, colour the bar in blue, external line of the bar in black, with a transparency of 0.5, and edit the title
ggplot(hdro, aes(x = HDI)) + geom_histogram(fill = "Blue",
                                            alpha = 0.5) + labs(title = "Human Development Index",
                                                              x= "HDI")

#Question 3
#what is the mean, the standard deviation and the median for the variable HDI
#please input the code here
mean(hdro$HDI)
sd(hdro$HDI)
median(hdro$HDI)
#please write a sentence here
mean of HDI is 0.7134307, standard deviation of HDI is 0.1508013 and median of HDI is 0.7277871 


# Question 4
#transfrom the variable Continent as a factor variable
hdro$Continent <- as.factor(hdro$Continent)

#Question 5
#Create a box blot of HDI, with each box representing a different continent
ggplot(hdro, aes(x = Continent)) + geom_boxplot()

#Question 6
#From the box plot create in Question 5, colors the boxes with different colors
ggplot(hdro, aes(x = Continent, color = Continent)) + geom_boxplot()

#Question 7
#What are the three things that need to be done before publishing this graph in a report?
#pls write your answer here



#Question 8
#Create a scatter plot showing the relation between HDI and Gini
ggplot(hdro, aes(x = HDI, y = Gini)) + geom_point()

#Question 9
#Add a title to the graph created in the previous Question
ggplot(hdro, aes(x = HDI, y = Gini)) + geom_point() + labs(title = "Relation between HDI and Gini",
                                                           x= "HDI")

#Question 10
#Given that high Gini means high degree of income inequality, 
#are the most developed countries more egalitarian or less egalitarian?
#Pls write an answer
Egalitarian, Since HDI goes higher, Gini value goes lower.

#Question 11
#Create a scatter plot showing the relation between HDI and Gini, with the dots colored depending on OECD, and a linear correlation line
#For this question the color of the dots need to be configurated in the geom part
ggplot(hdro, aes(x = HDI, y = Gini, color = OECD)) + geom_point()

#Question 12
#Add a meaningfull title to the graph created in 10
ggplot(hdro, aes(x = HDI, y = Gini, color = OECD)) + geom_point() + labs(title = "HDI and Gini Relations between member of OECD and Non-member of OECD",
                                                           x= "HDI")

#Question 13
#Create a bar plot showing how human_freedom_status within different Continent, with position dodge
ggplot(hdro, aes(fill=Human_freedom_status,x=Continent)) + geom_bar(position="dodge")

#Question 14
#Create a bar plot showing how human_freedom_status within different, with position fill
ggplot(hdro, aes(fill=Human_freedom_status,x=Human_freedom_status)) + geom_bar(position="fill")

#Question 15
#Which of those two positions is more appropriate if you want to communicate about the situation of human freedom within different continent
#Pls give your answer and justify it

I think in question 13 is better
