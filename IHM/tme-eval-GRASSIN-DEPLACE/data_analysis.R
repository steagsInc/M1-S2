library(plyr)
library(dplyr)
library(ggplot2)
library(ez)

#charger le fichier CSV
results <- read.csv("/home/steags/Documents/Master/M1-S2/IHM/tme-eval-GRASSIN-DEPLACE/experiment/logs/results.csv",sep=",")
filtered <- filter(results,Result == 1)
type <- group_by(filtered, Type,Number)
grouped <- summarise(type,count=n(),Mean=mean(Time),Sd=sd(Time))
# visualiser vos données
Se = grouped[1:6,"Sd"]/sqrt(grouped[1:6,"count"])
ci = Se*qt(0.95 / 2 + 0.5, 3 -1) 
ci = ci[1:6,"Sd"]

dodge <- position_dodge(width = 0.9)
g <- ggplot(grouped, aes(x = Type,y=Mean,fill=factor(Number)))
g + geom_bar(position = dodge,stat = "identity",width=0.8)+ geom_errorbar(aes(ymax=Mean+ci,ymin=Mean-ci),position = dodge,width=0.2)
ggsave(path = "/home/steags/Documents/Master/M1-S2/IHM/tme-eval-GRASSIN-DEPLACE/",filename = "bar.png",device="png")
# analyser vos données avec ANOVA
anova = ezANOVA(results,.(Time),.(ID),.(Type,Number))
a <- ggplot(as.data.frame(anova),aes(x=ANOVA.Effect,y=ANOVA.F))
a + geom_bar(stat="identity",width=0.6,fill="steelblue")+ geom_errorbar(aes(ymax=ANOVA.F+ANOVA.p,ymin=ANOVA.F-ANOVA.p),width=0.2)
ggsave(path = "/home/steags/Documents/Master/M1-S2/IHM/tme-eval-GRASSIN-DEPLACE/",filename = "anova_bar.png",device="png")
pairwise.t.test(results$Time,results$Type,p.adj="none")
