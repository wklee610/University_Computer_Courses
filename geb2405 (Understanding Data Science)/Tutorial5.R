#tutorial 5 -script
#Exercise 1
#1.1#
ggplot(smoking_and_drug_use_amongst_English_pupils,aes(x=AlAge2))+geom_histogram(fill="Blue",stat="count")
#1.2
ggplot(smoking_and_drug_use_amongst_English_pupils,aes(x=AlAge2))+geom_histogram(fill="Blue",stat="count", alpha=0.75)+labs(title="Age at which English pupils drunk alcohol for the first time",x="Age")


#Exercise 2
#2.1
ggplot(smoking_and_drug_use_amongst_English_pupils,aes(x=Books2))+geom_bar()
#2.2 
ggplot(smoking_and_drug_use_amongst_English_pupils,aes(fct_infreq(Books2)))+geom_bar()

#.2.3
ggplot(smoking_and_drug_use_amongst_English_pupils,aes(fct_infreq(Books2),fill=Books2))+geom_bar(alpha=0.5)+scale_fill_brewer(palette="Greens")+labs(title="Nbr of books that english pupils have at home",x="")

#Exercise 3
#3.1
ggplot(smoking_and_drug_use_amongst_English_pupils,aes(x=AlAge2,fill=Sex))+geom_histogram(stat="count", alpha=0.75)+labs(title="Age at which English pupils experienced alcohol for the first time", x="Age")
#3.2
#the distribution is very close for both sex
#3.3
ggplot(smoking_and_drug_use_amongst_English_pupils,aes(x=CgAge2,fill=Sex))+geom_density(stat="count",alpha=0.25)+labs(title="Age at which English pupils smoke cigarette for the first time", x="Age")


