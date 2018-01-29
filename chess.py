
# coding: utf-8

# In[28]:


import operator
import pandas
from subprocess import call

K = 32
elos = {}
record = {}

ledger = [line.strip() for line in open("chess.txt").read().split(",")]
for line in ledger:
    p1, outcome, p2 = line.split(" ")
    if not p1 in elos:
        elos[p1] = [1500,0,0,0]
    if not p2 in elos:
        elos[p2] = [1500,0,0,0]
    pre_1 = elos[p1][0]
    pre_2 = elos[p2][0]
    expected_1 = 1./(10.**(-(pre_1-pre_2)/400.)+1)
    expected_2 = 1./(10.**(-(pre_2-pre_1)/400.)+1)
    new_1 = 0
    new_2 = 0
        
    if outcome == "beat":
        new_1 = pre_1 + K*(1 - expected_1)
        new_2 = pre_2 + K*(0 - expected_2)
        elos[p1][1] += 1
        elos[p2][2] += 1
        
    if outcome == "tied":
        new_1 = pre_1 + K*(.5 - expected_1)
        new_2 = pre_2 + K*(.5 - expected_2)
        elos[p1][3] += 1
        elos[p2][3] += 1
        
    elos[p1][0] = new_1
    elos[p2][0] = new_2
        
pandas.options.display.precision = 0
df = pandas.DataFrame.from_dict(elos, 'index').sort_values(by=0, ascending=False)
df.columns = ['Elo','W','L','T']
df
head = """<!DOCTYPE HTML><html><head><link rel='stylesheet' type='text/css' href='style.css'></head><body style='margin: 50px'>"""
tail = "</body></html>"

output = open("chess.html", 'w')
output.writelines([head, df.to_html(border=1), tail])
output.close()

call(['scp', 'chess.txt' 'polylog1:public_html/chess.txt'])
call(['scp', 'chess.html' 'polylog1:public_html/chess.html'])
