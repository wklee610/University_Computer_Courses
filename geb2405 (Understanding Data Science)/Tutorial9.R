#exercise 1
millemium_2015_study<-millemium_2015_study%>%mutate_if(is.character,as.factor)
millemium_2015_study$class<-factor(millemium_2015_study$class,levels=c("Hi manag/prof","Lo manag/prof","Intermediate","Small emp and s-emp","Low sup and tech","Routine","Semi routine"))
table(millemium_2015_study$class)
table(millemium_2015_study$help)
millemium_2015_study$help<-factor(millemium_2015_study$help,levels = c("always","usually","sometimes","never or almost never"))
table(millemium_2015_study$help)
#Exercise 2
sjt.xtab(millemium_2015_study$class,millemium_2015_study$help,show.exp = TRUE,show.row.prc = TRUE)
#we can reject the hypothesis that parents tutoring does not depends on parents socio-economical status at 99.9% CI. 
#However, the correlation between the parents tutoring and socio-economic background is weak, sinc ethe cramer's V is below 0.1
#Dependeing of the version of GDA tools
#Old version
x<-table(millemium_2015_study$class,millemium_2015_study$help)
pem(x)
#newest version
pem(millemium_2015_study$class,millemium_2015_study$help)
# We can observe that the parents which are intermediary profession and lower professional are more likely to report that they "never or almost never" tutor their child homework
#On the contrary the small employer and own account worker have an higher propensity for always tutoring their child homework
#These are the three configurations for which the pem is below -10.
#At a general level, the parents from different social classes seem to differently tutoring their children homework since we can reject the null hypothesis (independance between class and help) at 99.9% CI
#However, the correlation between the two variable is quite low, since the cramer's V is largely below 0.1.
#Indeed, in almost all social classes, parents are around 70% to always or usually tutoring their child homework. Paradoxally the parents which are intermediate profession have an slightly higher (pem=6.5) propension to always supervise their child howmework
#and are more likely to never or almost never tutor their child homework.
#there is different hypothesis that can explain the absence of strong correlation. May be the year grade of the child might be taken into consideration. 
#Mother might be more likely to tutor their child than father. Further analysis might be required. Besides, it is possible that parents reply to provide a good image of themselves rather than reporting their actual behaviour.
#Finally, usually, and sometimes is not an objective enought criteria.

#Exercise 3
table(millemium_2015_study$inter)
millemium_2015_study$inter<-factor(millemium_2015_study$inter,levels = c("All of the time","Most of the time","Some of the time","Never"))
sjt.xtab(millemium_2015_study$class,millemium_2015_study$inter,show.exp = TRUE,show.row.prc = TRUE)
#we can reject the null hypothesis that is the independence between student interest for school and their socio-economic background
#However the correlation is quite weak since the cramer's V is about 0.058
#PEm old version
y<-table(millemium_2015_study$class,millemium_2015_study$inter)
pem(y)
#PEm new version
pem(millemium_2015_study$class,millemium_2015_study$inter)
#From the pem we can see that the soon and daughter of higher professional are less likely to be bored at school (-62.5% for Never)
#Similar phenomenon can be noticed for the soon and daughter of lower professional.
#In other words, the children who grown up in family where parents have more cultural capital are less likely to reject the school culture, which somehow echoes their familial culture
#The son and daughter of small employers and self employed are not in conflict with the school culture as it is postulated by Willis in learning from labour
#They are just slightly more likely to declare never be bored at school, while they have an lower propensity to find the course boring "most of the time"