import pandas as pd
import numpy as np
import csv

with open('speeches_mean_file.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists
        f.close() #close the csv
result = []
name_list = ['clinton', 'sanders', 'ted_cruz','trump','kasich' , 'carson','fiorina', \
            'bush', 'martin', 'chris', 'paul', 'robio', ]
for person in name_list:
    val = []
    dim = []
    for line in data:
        if line[0] == person:
            dim.append(line[1])
            val.append(float(line[2])+ 1 ) # shift mean from 0 to 1
    result.append([person, val])

##
##    
##df = pd.read_csv("speeches_mean_file.csv")
##print (df)
##g = df.groupby("candidate")
##data = g.groups
##
##print (data["trump"])
