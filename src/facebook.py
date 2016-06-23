import os
import csv

import numpy as np
import pandas as pd

from word_count import get_dict

def extract_posts(record,csvwriter,cand_num):
    lines =  record.split('\n')
    if cand_num<1:
        candidate = lines.pop(0).strip('"')
    else:
        candidate = lines.pop(1).strip('"')
    
    print candidate
    for l in lines:
        csvwriter.writerow([candidate,l.strip('"')])

if __name__ == '__main__':
    csvfile =  open(os.path.join(os.path.pardir,'data','facebook.csv'), 'wb')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['candidate','text'])

    items = []
    f = open(os.path.join(os.path.pardir,'data','Facebook_message.txt'),'rb')
    text = f.read().lower()
    per_cand = text.split('=======')
    for i,cand_record in enumerate(per_cand):
        record = extract_posts(cand_record,csvwriter,i)
