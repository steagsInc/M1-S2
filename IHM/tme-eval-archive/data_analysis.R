library(plyr)
library(ggplot2)
library(ez)

#charger le fichier CSV
results <- read.csv("/home/steags/Documents/Master/M1-S2/IHM/tme-eval-archive/experiment/logs/results.csv",sep=",")
filtered <- filter(results,Result == 1)
type <- group_by(filtered, Type,Number)
grouped <- summarise(type,count=n(),Mean=mean(Time),Sd=sd(Time))
# visualiser vos données
g <- ggplot(grouped, aes(x = interaction(Type,Number),y=Mean))
g + geom_bar(stat = "identity")

# analyser vos données avec ANOVA
