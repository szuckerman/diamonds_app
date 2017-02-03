library(dplyr)

diamonds_db <- src_sqlite("~/github_projects/diamonds_app/DIAMONDS.db", create = T)


# Add a diamond_id so we have a primary key

diamonds = diamonds %>%
mutate(
    diamond_id = row_number()
    )


#Index on the categorical values

copy_to(diamonds_db, diamonds, temporary = FALSE, indexes = list('cut', 'color', 'clarity'))



# Use the following to get the max length of each field when creating the DB model

diamonds %>%
summarize(
    cut = cut %>% as.character %>% nchar %>% max,
    color = color %>% as.character %>% nchar %>% max,
    clarity = clarity %>% as.character %>% nchar %>% max)

