suppressPackageStartupMessages(
  require(tidyverse)
)

mistress <- read_csv('data/cleansed/mistress_20201216.csv',
                     col_types = cols())

targeted <- mistress %>% 
  select(who_id, who_code, targeted) %>% 
  rename(value = targeted)

separate_values <- function(data, sep, new_col_len = 100){
  
  res <- data %>% 
    separate(value, into = as.character(1:new_col_len), sep = sep, extra = "merge", fill = "right") %>% 
    pivot_longer(!c(who_id, who_code), 'type', 'value') %>% 
    select(-type) %>% 
    drop_na(value)
  
  return(res)
  
}

res <- targeted %>% 
  separate_values(', ') %>% 
  separate_values(',') %>% 
  separate_values(' - ') %>% 
  separate_values(' / ') %>% 
  separate_values(' and ') %>%
  separate_values('; ')


write_csv(res, 'data/manual/targeted_summary_table.csv')
