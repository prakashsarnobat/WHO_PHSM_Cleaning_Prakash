# Script to identify values present in ID columns that are not present in WHO_ID

m <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/cleansed/mistress_latest.csv',
              col_types = manual_arranged_dtypes)




duplicate_missing <- setdiff(m$duplicate_record_id, m$who_id)

duplicate_missing <- m %>% filter(duplicate_record_id %in% duplicate_missing)


prev_missing <- setdiff(m$prev_measure_number, m$who_id)

prev_missing <- m %>% filter(prev_measure_number %in% prev_missing)

prev_missing %>% filter(who_code != '12')

follow_missing <- setdiff(m$following_measure_number, m$who_id)

follow_missing <- m %>% filter(following_measure_number %in% follow_missing)

follow_missing %>% filter(who_code != '12')

29


duplicate_missing %>% 
  group_by(who_code) %>% 
  dplyr::summarise(n = n())

prev_missing %>% 
  group_by(who_code) %>% 
  dplyr::summarise(n = n())

follow_missing %>% 
  group_by(who_code) %>% 
  dplyr::summarise(n = n())




