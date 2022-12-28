import pandas as pd
from config import *

df = pd.read_excel(f"data/{NAME}_output.xlsx")

# descriptive

sort_by = ['Junior', 'Mid', 'Senior', 'Expert']
df['experience_low'].value_counts(
    normalize=True).reindex(sort_by).reset_index()
df['experience_high'].value_counts(
    normalize=True).reindex(sort_by).reset_index()

# salaries
expert = df[df['experience_high'] == 'Expert']
expert['UoP_cash_high'].median()
expert['UoP_cash_low'].median()
expert['B2B_cash_high'].median()
expert['B2B_cash_low'].median()

senior = df[df['experience_high'] == 'Senior']
senior['UoP_cash_high'].median()
senior['UoP_cash_low'].median()
