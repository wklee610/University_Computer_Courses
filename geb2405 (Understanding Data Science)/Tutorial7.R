library("gmodels")

#exercise 1
CrossTable(Survey_GE_class_choice_1$Followed_GEC,prop.t=TRUE)
df_piechart<-data.frame(GEC=c("History of China","Societies inequalities","Western economic and law"),n=c(20,19,20),prop=c(33.9,32.2,33.9))
ggplot(df_piechart,aes(x="",y=prop,fill=GEC))+geom_bar(width=1,stat="identity",color="white")+coord_polar("y",start=0)+geom_text(aes(label=paste0(round(prop),"%")),position=position_stack(vjust=0.5))+theme(panel.background = element_blank(),axis.text = element_blank(),axis.line = element_blank(),axis.ticks = element_blank(),axis.title = element_blank(),plot.title = element_blank())
Survey_GE_class_choice_1_women<-subset(Survey_GE_class_choice_1,Gender=="Female")
Survey_GE_class_choice_1_men<-subset(Survey_GE_class_choice_1,Gender=="Male")
table(Survey_GE_class_choice_1_women$Followed_GEC)
table(Survey_GE_class_choice_1_men$Followed_GEC)
df_piechart_women<-data.frame(GEC=c("History of China","Societies inequalities","Western economic and law"),n=c(17,9,4),prop=c(56.7,30.0,13.3))
ggplot(df_piechart_women,aes(x="",y=prop,fill=GEC))+geom_bar(width=1,stat="identity",color="white")+coord_polar("y",start=0)+geom_text(aes(label=paste0(round(prop),"%")),position=position_stack(vjust=0.5))+theme(panel.background = element_blank(),axis.text = element_blank(),axis.line = element_blank(),axis.ticks = element_blank(),axis.title = element_blank(),plot.title = element_blank())
df_piechart_men<-data.frame(GEC=c("History of China","Societies inequalities","Western economic and law"),n=c(3,10,16),prop=c(10.3,34.4,55.17))
ggplot(df_piechart_men,aes(x="",y=prop,fill=GEC))+geom_bar(width=1,stat="identity",color="white")+coord_polar("y",start=0)+geom_text(aes(label=paste0(round(prop),"%")),position=position_stack(vjust=0.5))+theme(panel.background = element_blank(),axis.text = element_blank(),axis.line = element_blank(),axis.ticks = element_blank(),axis.title = element_blank(),plot.title = element_blank())

#Exercise 2
ggplot(Survey_GE_class_choice_1,aes(x=Major,fill=Followed_GEC))+geom_bar(position="fill")+facet_wrap(~Gender)
ggplot(Survey_GE_class_choice_1,aes(x=Major,fill=Followed_GEC))+geom_bar(position="fill")+facet_wrap(~Gender)+theme(axis.text.x = element_text(angle = 45,size=8,vjust=0.7))+labs(x="")
ggplot(Survey_GE_class_choice_1,aes(x=Major,fill=Followed_GEC))+geom_bar(position="fill",alpha=0.7)+facet_wrap(~Gender)+theme(axis.text.x = element_text(angle = 45,size=8,vjust=0.7))+labs(x="")+scale_fill_manual(values=c("Red","Blue","Green"))

#Exercise 3
ggplot(Survey_GE_class_choice_1,aes(x=Major,fill=Project_after_graduate))+geom_bar(position="fill")+facet_wrap(~Gender)
#The proportion of people willing to find a job after graduation is 0 for both male and female in management and economics.
#Within the SME students a difference exist for the country where student went to continue their study. The female are more likely to mention UK while the male are more likely to mention US for postgraduate study.
#SSE students are more likely to find a job after their undergraduate program, especially female students.

#Exercise 4
#supplementary exercise for those who are quick
#see https://stackoverflow.com/questions/18537378/faceted-piechart-with-ggplot2
ggplot(Survey_GE_class_choice_1,aes(x = factor(1),fill=factor(Project_after_graduate))) + facet_wrap(~Gender) + geom_bar(width = 1,position = "fill") + coord_polar(theta="y")
ggplot(Survey_GE_class_choice_1,aes(x = factor(1),fill=factor(Project_after_graduate))) + facet_wrap(~Rank) + geom_bar(width = 1,position = "fill") + coord_polar(theta="y")
