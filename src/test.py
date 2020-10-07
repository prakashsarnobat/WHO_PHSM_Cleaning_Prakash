import pandas as pd

print("Reading data...")
df = pd.read_csv(
    "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"
)

print("Writing data...")
df.to_csv("./output/jh_hit.csv")

print("Success.")
