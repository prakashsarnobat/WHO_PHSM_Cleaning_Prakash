master <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/tmp/master/master.csv',
                   col_types = manual_arranged_dtypes)


df <- master %>% 
  filter(processed == 'not_cleansed') %>% 
  group_by(dataset, who_code) %>% 
  dplyr::summarise(n = n()) %>% 
  mutate(data_code = paste0(dataset, '_', who_code))

df %>% 
  arrange(-n)

df %>% 
  ggplot() + 
  geom_bar(aes(x = data_code, y = n, fill = dataset), stat = 'identity') + 
  theme_classic() + 
  theme(axis.text.x = element_text(angle = 90))

master %>% 
  filter(who_code == '1.4', dataset == 'OXCGRT') %>% 
  group_by(country_territory_area) %>% 
  dplyr::summarise(n = n()) %>% 
  arrange(-n)

master %>% 
  filter(dataset == 'JH_HIT') %>% 
  filter(processed == 'not_cleansed') %>% 
  group_by(dataset, country_territory_area, who_code) %>% 
  dplyr::summarise(n = n()) %>% 
  arrange(-n) 
