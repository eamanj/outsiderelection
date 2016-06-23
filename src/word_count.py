import sys
import os

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
        df.ix[i,'prob_gender']  = temp/tl 
    df['prob_gender'] = stats.zscore(df['prob_gender'])
    return df

def main2(typ='gender'):
    df = pds.read_csv(os.path.join(os.path.pardir,'data','speeches.csv'))
    word_dict = get_dict(typ)
    update_df(df,word_dict)
    plot(df.prob_gender,'overall_{0}.png'.format(typ))
    
    clinton = df[df.candidate=='clinton']['prob_gender']
    plot(clinton.values,'clinton_{0}.png'.format(typ))
    
    clinton = df[df.candidate=='sanders']['prob_gender']
    plot(clinton.values,'sanders_{0}.png'.format(typ))

def main():
    df = pds.read_csv(os.path.join(os.path.pardir,'data','speeches.csv'))
    overall_hist = compute_dist(df,word_dict)
    
    temp_record = candidate_record(df,'clinton')
    clinton_hist = compute_dist(temp_record,word_dict)
    
    temp_record = candidate_record(df,'sanders')
    sanders_hist = compute_dist(temp_record,'sanders')
    
    plot(overall_hist,'overall.png')
    #plot(clinton_hist,'clinton.png')
    #plot(sanders_hist,'sanders.png')
    
    #print stats.entropy(overall_hist, qk=clinton_hist, base=None)
    #print stats.entropy(overall_hist, qk=sanders_hist, base=None)
if __name__ == '__main__':
    main2('gender')
    main2('money')
     
    
