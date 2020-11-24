acaps <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/raw/ACAPS_latest.csv') %>% 
  select(ID, DATE_IMPLEMENTED) %>% 
  mutate(ID = as.character(ID)) %>% 
  mutate(DATE_IMPLEMENTED = lubridate::dmy(DATE_IMPLEMENTED))

acaps

m <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/output/master_2020_11_20.csv')

m %>% 
  filter(processed == 'sequenced') %>% 
  filter(dataset == 'ACAPS') %>% 
  select(prop_id, date_start) %>% 
  left_join(acaps, by = c('prop_id' = 'ID'))
