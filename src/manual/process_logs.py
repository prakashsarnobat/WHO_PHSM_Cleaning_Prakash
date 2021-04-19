logs = open("/Users/hamishgibbs/Documents/Covid-19/PHSM/WHO_PHSM_Cleaning/tmp/process/process.log", 'r').readlines()

categories = []

for line in logs:

    try:
        category = line.split("prov_category: ")[1].split(" ")[0]
        subcategory = line.split("prov_subcategory: ")[1].split(" ")[0]
        measure = line.split("prov_measure: ")[1].replace("\n", "")
        categories.append(category + " " + subcategory + " " + measure)
    except:
        pass

categories

len(categories)
