import pandas as pd
df=pd.read_csv("data/evenements.csv", sep=";")
print(df.shape)
print(df.columns.tolist())
print(df.isna().sum())
print(df[["title","date_start","date_end","address_zipcode", "lat_lon","price_type"]].head(10))
print(df["price_type"].value_counts(dropna=False))
print((df["lat_lon"]== "0.0, 0.0").sum())
