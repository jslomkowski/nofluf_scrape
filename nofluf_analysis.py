import pandas as pd
import json
from config import *


def remove_list_duplicates():
    df = pd.read_csv(f'data/{NAME}_nofluffjobs_urls.csv')
    df.drop_duplicates(inplace=True)
    df.to_csv(f'data/{NAME}_nofluffjobs_urls.csv', index=False)
    return df


df = remove_list_duplicates()

# df = pd.read_excel('data/result.xlsx')
df = pd.read_csv(f'data/{NAME}_result.csv')
len(df['key'].unique()) / 20

df['value'] = df['value'].str.lower()

# map inpropper values to propper
with open('data/name_mapping.json', 'r') as f:
    name_mapping = json.load(f)
df['value'] = df['value'].replace(name_mapping)

# split data into two groups: structured and unstructured
move = [
    'specs', 'benfs', 'primary_req', 'envs', 'secondary_req', 'gear',
    'locations', 'tasks']
unstructured_perks = df[df['variable'].isin(move)]
structured_perks = df[~df['variable'].isin(move)]
structured_perks = structured_perks.pivot(
    index='key', columns='variable', values='value').reset_index()

# change datatypes to int
dtypes_change = ['B2B_cash_high', 'B2B_cash_low', 'UZ_cash_high', 'UZ_cash_low',
                 'UoP_cash_high', 'UoP_cash_low']
for c in dtypes_change:
    structured_perks[c] = structured_perks[c].astype(pd.Int32Dtype())

# change order of columns
structured_perks = structured_perks[[
    'timestamp', 'key', 'title', 'company', 'level_high', 'level_low',
    'posting_time', 'remote', 'B2B_cash_currency', 'B2B_cash_high',
    'B2B_cash_low', 'UZ_cash_currency', 'UZ_cash_high', 'UZ_cash_low',
    'UoP_cash_currency', 'UoP_cash_high', 'UoP_cash_low', 'link'
]]

# save
with pd.ExcelWriter(f'data/{NAME}_result.xlsx') as writer:
    structured_perks.to_excel(
        writer, sheet_name='structured_perks', index=False)
    unstructured_perks.to_excel(
        writer, sheet_name='unstructured_perks', index=False)
