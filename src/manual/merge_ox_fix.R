mis <- readxl::read_xlsx("/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/cleansed/mistress_latest.xlsx")

m <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/tmp/master/master.csv',
              col_types = cols(prov_category = col_character(),
                               prov_subcategory = col_character(),
                               prov_measure = col_character()))
m %>% 
  group_by(dataset, processed) %>% 
  summarise(n = n())

mis_cs <- mis %>% 
  filter(dataset == 'OXCGRT') %>% 
  mutate(combo_string = paste(iso, dataset, date_start, sep = '_')) %>% 
  pull(combo_string)

m_cs <- m %>% 
  filter(dataset == 'OXCGRT') %>% 
  mutate(combo_string = paste(prop_id,
                              country_territory_area,
                              dataset,
                              area_covered,
                              who_code,
                              date_start, sep = '_')) %>% 
  pull(combo_string)


length(setdiff(mis_cs, m_cs))
length(setdiff(m_cs, mis_cs))

m %>% 
  filter(processed == 'not_cleansed') %>% 
  group_by(dataset) %>% 
  summarise(n = n())

m %>% 
  filter(who_code == 'unknown') %>% 
  mutate(prov_category = paste0("X", prov_category, "X"),
         prov_subcategory = paste0("X", prov_subcategory, "X"),
         prov_measure = paste0("X", prov_measure, "X")) %>% 
  select(prop_id, prov_category, prov_subcategory, prov_measure) %>% view


ox <- read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv')


man <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/tmp/manually_cleaned/records.csv')

post <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/tmp/postprocess/records.csv')

lu <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/data/merge/update_merge_2021_03_10.csv') %>% 
  select(prop_id, country_territory_area, dataset, area_covered, who_code, date_start)

man$date_start %>% class
post$date_start %>% class
lu$date_start %>% class

lu_cs <- lu %>% 
  filter(dataset == 'OXCGRT') %>% 
  mutate(combo_string = paste(prop_id,
                              country_territory_area,
                              dataset,
                              area_covered,
                              who_code,
                              date_start, sep = '_'))

man_cs <- man %>% 
  filter(dataset == 'OXCGRT') %>% 
  mutate(combo_string = paste(prop_id,
                              country_territory_area,
                              dataset,
                              area_covered,
                              who_code,
                              date_start, sep = '_'))

post_cs <- post %>% 
  filter(dataset == 'OXCGRT') %>% 
  mutate(combo_string = paste(prop_id,
                              country_territory_area,
                              dataset,
                              area_covered,
                              who_code,
                              date_start, sep = '_'))

post_lu_cs <- setdiff(post_cs$combo_string, lu_cs$combo_string)
post_man_cs <- setdiff(post_cs$combo_string, man_cs$combo_string)

post_cs %>% 
  filter(combo_string %in% post_lu_cs) %>% 
  group_by(who_code) %>% 
  summarise(n = n())
   

post <- read_csv('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/tmp/postprocess/records.csv')

