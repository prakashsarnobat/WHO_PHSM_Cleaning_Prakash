# Script to merge updates from mpast datasets.

# NEEDS work and more reliability
# hotfix 2020 11 25

columns <- c("prop_id", "country_territory_area", "dataset", "area_covered", "who_code", "date_start")

m_update <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/not_cleansed/update_merge_2020_11_25.csv')

m_update <- m_update %>% 
  select(columns)

m <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/not_cleansed/master_2020_11_25.csv')

#m %>% filter(original_who_code == '12')

m <- m %>% 
  filter(processed == 'not_cleansed') %>% 
  select(columns)

m_update <- rbind(m, m_update)

write_csv(m_update, '/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/not_cleansed/update_merge_2020_12_02.csv')
  


#m <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/output/master_2020_11_25.csv')


#m %>% filter(keep == 'y', processed == 'sequenced')

