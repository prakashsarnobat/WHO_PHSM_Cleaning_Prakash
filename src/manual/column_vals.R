jh <- read_csv('https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv') 


jh <- jh %>% 
  select(update, national_entry, status, 
         status_simp, subpopulation, required, 
         reduced_capacity, symp_screening,
         entry_quality) %>% 
  mutate(n = row_number()) %>% 
  pivot_longer(!n, names_to = "column", values_to = "value") %>% 
  select(-n) %>% 
  distinct() %>% 
  arrange(column) %>% 
  mutate(dataset = 'JH_HIT')

write_csv(jh, '/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/config/input_check/coded_values/JH_HIT.csv')

acaps <- readxl::read_xlsx('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/raw_data/ACAPS_latest.xlsx', sheet = 2)

acaps <- acaps %>% 
  select(`Action taken`, `Focus area`, `Mandatory`, `Subnational/regional only`) %>% 
  mutate(n = row_number()) %>% 
  pivot_longer(!n, names_to = "column", values_to = "value") %>% 
  select(-n) %>% 
  distinct() %>% 
  arrange(column) %>% 
  mutate(dataset = 'ACAPS')

write_csv(acaps, '/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/config/input_check/coded_values/ACAPS.csv')

cdc <- readxl::read_xlsx('/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/raw_data/CDC_ITF_latest.xlsx', sheet = 2)

cdc <- cdc %>% 
  select(`Action taken`, `Focus area`, `Mandatory`, `Subnational/regional only`) %>% 
  mutate(n = row_number()) %>% 
  pivot_longer(!n, names_to = "column", values_to = "value") %>% 
  select(-n) %>% 
  distinct() %>% 
  arrange(column) %>% 
  mutate(dataset = 'CDC_ITF')

write_csv(cdc, '/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/config/input_check/coded_values/CDC_ITF.csv')




