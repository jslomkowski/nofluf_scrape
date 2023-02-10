import pandas as pd
from config import *


df = pd.read_excel(f"data/results/{NAME}/{NAME}_output.xlsx")

# df_lite = df[["link", "primary_skils"]].reset_index(drop=True)
df_lite = pd.concat([df[["link"]], df['primary_skils'].str.split(",", expand=True)], axis = 1)
df_lite["count"] = 1

cols = df_lite.columns[1:]

# cols = [str(x) for x in cols]


df_lite.pivot(index="link", columns=cols, values="count")