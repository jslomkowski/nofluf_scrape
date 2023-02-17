
import pandas as pd
import itertools
from config import NAME


df = pd.read_excel(fr"data\results\{NAME}\{NAME}_output.xlsx")

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
