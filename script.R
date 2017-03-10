library(ggplot2)
library(reshape2)

args = commandArgs(TRUE)

d <- read.table(file=paste(args[1],".sample_interval_statistics", sep=""), header=T)
d
d <-melt(d)
d
#d$rowid <- 1:args[4]
d
ggplot(d, aes(variable, value, group=factor(id))) + geom_line(aes(color=factor(id))) + coord_cartesian(xlim = c(0, 50)) + geom_vline(xintercept=10)
ggsave(args[2])

d <- read.table(file=paste(args[1],".sample_cumulative_coverage_proportions", sep=""), header=T)
d
d <-melt(d)
d
#d$rowid <- 1:args[4]
d
ggplot(d, aes(variable, value, group=factor(id))) + geom_line(aes(color=factor(id))) + coord_cartesian(xlim = c(0, 50)) + geom_vline(xintercept=10)
ggsave(args[3])