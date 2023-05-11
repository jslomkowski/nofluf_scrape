import pandas as pd
import itertools
from config import NAME


df = pd.read_excel(
    fr"data\results\{NAME}\{NAME}_output.xlsx", sheet_name="Sheet1")

# set experience
# exp = ['Expert', 'Senior', 'Mid', 'Junior', 'Trainee']
exp = ['Senior', 'Mid']

# df = df[(df['experience_low'].isin(exp)) & (df['experience_high'].isin(exp))]
df = df[(df['experience_high'].isin(exp))]


def count_skills(df, column_name):
    skills = list(df[column_name].str.split(", "))
    skills = list(itertools.chain.from_iterable(skills))
    skills = list(set(skills))
    skills_df = pd.DataFrame(columns=skills)
    df_split = df[column_name].str.split(", ", expand=True)

    for i in range(len(df_split)):
        _df = pd.DataFrame(df_split.iloc[i]).T
        _df.dropna(axis=1, how="all", inplace=True)
        _df.columns = _df.values.tolist()[0]
        skills_df = pd.concat([skills_df, _df], axis=0)

    skills_count = skills_df.count().sort_values(ascending=False)
    skills_count = pd.DataFrame(skills_count, columns=["count"])
    return skills_count


top_skills_count = count_skills(df, "primary_skils")[:15]
print(top_skills_count)

secondary_skills_count = count_skills(df, "secondary_skils")[:15]
print(secondary_skills_count)
