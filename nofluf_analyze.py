
import pandas as pd
import itertools
from config import NAME


df = pd.read_excel(fr"data\results\{NAME}\{NAME}_output.xlsx")
df = df[df['experience_low'] == 'Senior']
df = df[df['experience_high'] == 'Senior']

top_skils = list(df["primary_skils"].str.split(", "))
top_skils = list(itertools.chain.from_iterable(top_skils))
top_skils = list(set(top_skils))
top_skils = pd.DataFrame(columns=top_skils)
df_split = df["primary_skils"].str.split(", ", expand=True)

for i in range(len(df_split)):
    # print(i)
    # i = 100
    _df = pd.DataFrame(df_split.iloc[i]).T
    _df.dropna(axis=1, how="all", inplace=True)
    _df.columns = _df.values.tolist()[0]
    top_skils = pd.concat([top_skils, _df], axis=0)

top_skils = top_skils.count().sort_values(ascending=False)
top_skils = pd.DataFrame(top_skils, columns=["count"])
print(top_skils[:15])

secondary_skils = list(df["secondary_skils"].str.split(", "))
secondary_skils = list(itertools.chain.from_iterable(secondary_skils))
secondary_skils = list(set(secondary_skils))
secondary_skils = pd.DataFrame(columns=secondary_skils)
df_split = df["secondary_skils"].str.split(", ", expand=True)

for i in range(len(df_split)):
    # print(i)
    # i = 100
    _df = pd.DataFrame(df_split.iloc[i]).T
    _df.dropna(axis=1, how="all", inplace=True)
    _df.columns = _df.values.tolist()[0]
    secondary_skils = pd.concat([secondary_skils, _df], axis=0)

secondary_skils = secondary_skils.count().sort_values(ascending=False)
secondary_skils = pd.DataFrame(secondary_skils, columns=["count"])
print(secondary_skils[:15])
