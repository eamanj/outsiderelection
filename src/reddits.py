import os
import sys
import csv

import pandas
import praw

from secret_key import client_id
redit = praw.Reddit(user_agent=client_id)

def get_text(subreddit_name):
    submissions = redit.get_subreddit(subreddit_name).get_top_from_all(limit=1)
    sub_objs = [x for x in submissions] 
    data = []
    for x in sub_objs: 
        #t = x.title.encode('utf-8')
        #data.append(t)
        comments = praw.helpers.flatten_tree(x.comments)
        for c in comments:
            if not isinstance(c,praw.objects.MoreComments): 
                data.append(c.body.encode('utf-8'))
    return data

if __name__ == '__main__':
    subreddits = dict(trump = "The_Donald",
                    kasich = "KasichForPresident",
                    rubio = "marco_rubio",
                    bush = "JEB",
                    carson = "BenCarson",
                    clinton = "hillaryclinton",
                    sanders = "SandersForPresident")
    
    csvfile =  open(os.path.join(os.path.pardir,'data','reddits.csv'), 'wb')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['candidate','text'])
    for name, url in subreddits.iteritems():
        print name
        text_list = get_text(url)
        for text in text_list:
            row = [name, text] 
            csvwriter.writerow(row)
    csvfile.close()
