import pandas as pd
df=pd.read_csv("data/evenements.csv", sep=";")
cols=["title", "date_start", "date_end", "address_zipcode", "lat_lon", "event_indoor", "qfap_tags", "occurrences"]

for c in cols : 
	print(df[c].isna().sum())
print()
print(df["date_start"].head(3).tolist())
print(df["date_end"].head(3).tolist())
print(df["lat_lon"].head(3).tolist())
print(df["event_indoor"].value_counts(dropna=False))
print(df["qfap_tags"].head(5).tolist())
print(df["occurrences"].dropna().iloc[0][:300])
