master <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/output/master_2021_01_13.csv')


master$admin_level %>% unique()
master$who_code

t1 <- master %>% 
  mutate(total = 1,
         keep_y = ifelse(keep %in% c('y', 'Y'), T, F),
         national = ifelse(keep_y & admin_level == 'national', T, F),
         state = ifelse(keep_y & admin_level == 'state', T, F),
         other = ifelse(keep_y & admin_level == 'other', T, F)) %>% 
  group_by(who_code) %>% 
  summarise(total = sum(total, na.rm = T),
            keep_y = sum(keep_y, na.rm = T),
            national = sum(national, na.rm = T),
            state = sum(state, na.rm = T),
            other = sum(other, na.rm = T)) %>% 
  arrange(-total)
  


t2 <- master %>% 
  mutate(total = 1,
         keep_y = ifelse(keep %in% c('y', 'Y'), T, F),
         national = ifelse(keep_y & admin_level == 'national', T, F),
         state = ifelse(keep_y & admin_level == 'state', T, F),
         other = ifelse(keep_y & admin_level == 'other', T, F)) %>% 
  group_by(country_territory_area) %>% 
  summarise(total = sum(total, na.rm = T),
            keep_y = sum(keep_y, na.rm = T),
            national = sum(national, na.rm = T),
            state = sum(state, na.rm = T),
            other = sum(other, na.rm = T)) %>% 
  arrange(-total)

write_csv(t1, '~/Downloads/summary_table_who_code.csv')
write_csv(t2, '~/Downloads/summary_table_country.csv')

master %>% filter(who_code %in% c('10', '13'), keep %in% c('y', 'Y')) %>% pull(who_id)

master %>% filter(country_territory_area == 'United States Of America',
                  keep %in% c('y', 'Y'),
                  admin_level == 'state')
