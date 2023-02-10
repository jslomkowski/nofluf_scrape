
import pandas as pd
import itertools
import numpy as np
df = pd.read_excel("data/results/2023-02-09_ai_output.xlsx")

df_lite = df[["link", "primary_skils"]]

cols_lst = list(df_lite["primary_skils"].str.split(","))
cols_lst = list(itertools.chain.from_iterable(cols_lst))

# cols_lst = [x.lower() for x in cols_lst]
cols_lst = [x.strip() for x in cols_lst]
cols_lst = list(set(cols_lst))

df_cols_list = pd.DataFrame(columns=cols_lst)

df_lite_expanded = pd.concat(
    [df_lite['link'],
     df_lite["primary_skils"].str.split(",", expand=True)], axis=1)

df_lite_expanded = df_lite["primary_skils"].str.split(",", expand=True)

for i in range(len(df_lite_expanded)):
    print(i)
    i=0
    df_lite_ex = pd.DataFrame(df_lite_expanded.iloc[i]).T
    df_lite_ex.columns = df_lite_ex.values.tolist()[0]
    df_cols_list = df_cols_list.append(df_lite_ex)
    # ! TODO fix this