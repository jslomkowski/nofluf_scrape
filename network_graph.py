import os
import sys
import pandas as pd
import itertools
from pyvis.network import Network
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.realpath('..'))

primary_skils = pd.read_excel(r'C:\Users\x\git\nofluf_scrape\data\results\2023-02-10_back_end\2023-02-10_back_end_output.xlsx')
primary_skils = primary_skils['primary_skils']


lst = []
for i in primary_skils:
    # i = i.split(',')
    lst.append(list(itertools.combinations(i.split(', '), 2)))

lst = [item for sublist in lst for item in sublist]
# in lst count the number of times each tuple appears
final_lst = Counter(lst)
final_lst = sorted(final_lst.items(), key=lambda x: x[1], reverse=True)
# convert final_lst to list of tuples with string1, string2, int
final_lst = [(i[0][0], i[0][1], i[1]) for i in final_lst]
cuttof = 5
final_lst = [i for i in final_lst if i[2] > cuttof]
# get unique strings from final_lst
unique_strings = list(set([item for sublist in final_lst for item in sublist[:2]]))


g = Network(notebook=True, cdn_resources='in_line')
g.add_nodes(unique_strings,
            label=unique_strings)
g.add_edges(final_lst)

g.show_buttons(filter_="physics")
g.toggle_physics(True)

g.save_graph("example.html")
