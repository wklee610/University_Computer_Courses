#Graphing two continuous/numerical variables

#simple scatter plot with two variables
ggplot(Student_BMI_2, aes(x=BMI,y=GPA))+geom_point()
ggplot(Student_BMI_2, aes(x=BMI,y=GPA))+geom_point(size=3)
#Adding extra information using color and shape
ggplot(Student_BMI_2, aes(x=BMI,y=GPA,color=Gender))+geom_point(size=2)
ggplot(Student_BMI_2, aes(x=BMI,y=GPA,color=Gender,shape=Dpt))+geom_point(size=2)

#Practice 
#Visualize relation between BMI and homework_day
ggplot(Student_BMI_2,aes(y=BMI,x=homework_day))+geom_point(size=2,color="blue")
#visualize the relation between GPA and walk_meter_day
ggplot(Student_BMI_2,aes(y=BMI,x=walk_meter_day))+geom_point(size=2,color="blue")
#use color to show the difference by Department
ggplot(Student_BMI_2,aes(y=BMI,x=walk_meter_day,color=Dpt))+geom_point(size=2)
ggplot(Student_BMI_2,aes(y=BMI,x=homework_day,color=Dpt))+geom_point(size=2)

#adding a curve showing the tendency (loess curve or linear model)
ggplot(Student_BMI_2, aes(x=BMI,y=weight))+geom_point()+geom_smooth(method="lm")
ggplot(Student_BMI_2, aes(x=BMI,y=weight))+geom_point()+geom_smooth(method="loess")
#Let's Pratcice
#Add a loess curve
ggplot(Student_BMI_2,aes(x=BMI,y=homework_day))+geom_point(size=2)+geom_smooth(method="loess")
ggplot(Student_BMI_2,aes(x=BMI,y=walk_meter_day))+geom_point(size=2,color="blue")+geom_smooth(method="loess")

#Graphing a continuous variable vs a discrete one
#doing a bar boxplot: visualize the relation between BMI, department and gender
ggplot(Student_BMI_2,aes(x=Gender,y=BMI,color=Gender))+geom_boxplot()
#Practice
ggplot(Student_BMI_2,aes(x=Dpt,y=BMI,color=Dpt))+geom_boxplot()+labs(title="BMI of CUHK SZ Students in different department",x="Department")
ggplot(Student_BMI_2,aes(x=Dpt,y=BMI,color=Gender))+geom_boxplot()+labs(title="Boxplot of Students' BMI by Department and Gender", x="Department")

#Graphing two categorical variables
# bar chart of students origin per department
Student_BMI_2$`place of birth`<-as.factor(Student_BMI_2$`place of birth`)
ggplot(Student_BMI_2,aes(fill=`place of birth`,x=Dpt))+geom_bar(position="dodge")
#Do even better 
Student_BMI_2$`place of birth`<-factor(Student_BMI_2$`place of birth`,levels=c("Guangdong","Other_province","International"))
levels(Student_BMI_2$`place of birth`)
ggplot(Student_BMI_2,aes(fill=`place of birth`,x=Dpt))+geom_bar(position="dodge")

#prepare the data for analysis
Student_BMI_2$video_game<-as.factor(Student_BMI_2$video_game)
table(Student_BMI_2$video_game)

#Plot a bar chart using geom_bar video game vs Dpt
#Let's practice 
#Try two possible representation fro video game vs gender
ggplot(Student_BMI_2,aes(x=video_game,fill=Gender))+geom_bar(position="dodge")
ggplot(Student_BMI_2,aes(fill=video_game,x=Gender))+geom_bar(position="dodge")

#Try the position=stack and position=fill
ggplot(Student_BMI_2,aes(fill=video_game,x=Gender))+geom_bar(position="stack")
ggplot(Student_BMI_2,aes(fill=video_game,x=Gender))+geom_bar(position="fill")                                                     
#Let's Practice
#Are the students from different origin equally likely to play video games?
#make the plot and edit the titles
ggplot(Student_BMI_2,aes(fill=video_game,x=`place of birth`))+geom_bar(position="fill")
ggplot(Student_BMI_2,aes(fill=video_game,x=`place of birth`))+geom_bar(position="fill")+labs(title="Video games habits per students origin",y="Percentage")

                                                    