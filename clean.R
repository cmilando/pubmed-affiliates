# Run after run.py

library(tidyverse)

xx <- read.csv("articles_authors.csv", sep = "|", colClasses = 'character',
                 header = T, fill = NA)

xx2 <- xx %>%
  filter(DateCompletedYear %in% c('2020', '2021', '2022', '2024')) %>%
  distinct(Author.Last, Author.First.name, Affiliation)

write.table(xx2, file = "distinct2020-2024.txt", sep = "|", 
            quote = F, row.names = F)
