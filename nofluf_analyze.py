
import pandas as pd
import itertools

df = pd.read_excel(r"data\results\2023-02-10_back_end\2023-02-10_back_end_output.xlsx")

df_cols = list(df["primary_skils"].str.split(", "))
df_cols = list(itertools.chain.from_iterable(df_cols))
df_cols = list(set(df_cols))
df_cols = pd.DataFrame(columns=df_cols)
df_split = df["primary_skils"].str.split(", ", expand=True)

for i in range(len(df_split)):
    print(i)
    i = 100
    _df = pd.DataFrame(df_split.iloc[i]).T
    _df.dropna(axis=1, how="all", inplace=True)
    _df.columns = _df.values.tolist()[0]
    df_cols = pd.concat([df_cols, _df], axis=0)
