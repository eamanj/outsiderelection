import sys
import os
import csv

import numpy as np
import pandas as pds
import scipy.stats as stats
import matplotlib.pylab as plt


def get_dict(typ):
    words = None
    if typ=='gender':
        words =  ['men','man','male','boy','guy','husband','father','son','sir','gentleman',\
                'women','women','female','wife','girl','mother']
    if typ=='money':
        words = ['wallstreet','pac','money','donation','donations','doner','doners','finance','fec']
    if typ=='race':
        words = ['black','white','hispanic','asian','african american', 'caucasian',\
                 'ethnicity', 'native american', 'ethnic minority', 'brown people', 'ethnic']
    if typ=='other_countries_immigrants':
        words = ['mexico','china','mexican','chinese','cuba', 'korea', 'UK', 'europe', 'finland', 'norway'\
                 'canada', 'foreigners', 'immigrants', 'immigration', 'foreign', 'asia', 'south america' ]
    if typ=='swear':
        words = ['damn','shit','fuck','bitch','asshole', 'faggot', 'darn', 'cunt', 'motherfucker', 'gosh'\
                 'crap', 'piss', 'dick', 'cock', 'fag', 'pussy', 'bastard', 'slut', 'douche', 'bastard', \
                 'bloody', 'bugger', 'bollocks', 'arsehole' ]
    return words


def compute_dist(df,word_dict):
    text_list = df['text'].values
    #text = ''.join(temp)
    #text = text.lower()
    counts = []
    for text in text_list:
        tl = float(len(text))
        temp = [text.lower().count(keyword)/tl for keyword in word_dict]
        counts.extend(temp)
    return counts

def candidate_record(df,name):
    return df[df.candidate==name]

def plot(hist,fname,xlim_right=None):
    fig,ax = plt.subplots()
    ax.hist(hist)
    if xlim_right:
        ax.set_xlim(right=xlim_right)
    plt.savefig(os.path.join(os.path.pardir,'plots',fname))
    plt.close()


def update_df(df,word_dict):
    for i,r in enumerate(df.iterrows()):
        text = df.ix[i,'text'].lower()
        tl = float(len(text))
        temp = sum([text.count(keyword) for keyword in word_dict])
        df.ix[i,'prob']  = temp/tl 
    df['prob_zscore'] = stats.zscore(df['prob'])
    return df

def main2(df, typ, csvwriter):
    candidates = df.candidate.unique()
    
    word_dict = get_dict(typ)
    update_df(df,word_dict)
    plot(df.prob_zscore,'overall_{0}.png'.format(typ))
    for cand_name in candidates:
        cand_hist = df[df.candidate==cand_name]['prob_zscore']
        mean = np.mean(cand_hist)
        plot(cand_hist.values,'{0}_{1}.png'.format(cand_name,typ))
        row =  [cand_name,typ,mean]
        csvwriter.writerow(row)

def main():
    df = pds.read_csv(os.path.join(os.path.pardir,'data','speeches2.csv'))
    candidates = df.candidates.unique()

    overall_hist = compute_dist(df,word_dict)
    
    for cand_name in candidates:
        temp_record = candidate_record(df,cand_name)
        cand_hist = compute_dist(temp_record,word_dict)
        cand_mean = np.mean(cand_hist)
        plot(cand_hist,'clinton.png')

    
        
    
    
    plot(overall_hist,'overall.png')
    #plot(sanders_hist,'sanders.png')
    
    #print stats.entropy(overall_hist, qk=clinton_hist, base=None)
    #print stats.entropy(overall_hist, qk=sanders_hist, base=None)
if __name__ == '__main__':
    mean_file = open(os.path.join(os.path.pardir,'data','mean_file.txt'),'wb')
    csvwriter = csv.writer(mean_file)
    csvwriter.writerow(['candidate','dimention',',mean'])
    df = pds.read_csv(os.path.join(os.path.pardir,'data','speeches_selected.csv'))
     
    main2(df,'gender', csvwriter)
    main2(df,'money',csvwriter)
    main2(df,'swear',csvwriter)
    main2(df,'other_countries_immigrants',csvwriter)
    mean_file.close()
     
    
