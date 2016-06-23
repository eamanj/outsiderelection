from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import urllib2 as urllib
import os

import numpy as np
import csv


url_prefix = "http://www.presidency.ucsb.edu/"

def extract_speach_info(record):
    candidate = record[0].get_text()
    date = record[1].get_text()
    url = record[2].a['href'] #'../ws/index.php?pid=110044'
    url =  url[2:] #'/ws/index.php?pid=110044'
    link = "{0}{1}".format(url_prefix,url)
    #print link
    soup = get_soup(link)
    text = soup.find_all('span',class_='displaytext')[0].get_text().encode('utf-8')
    #print text
    #paragraphs = [p.getText() for p in text.find_all('p')]
    return [candidate,date,text]

def get_soup(url):
    r = urllib.urlopen(url)
    soup = BeautifulSoup(r)
    return soup

def add_trump(csvwriter):
    row_list = []
    for i in xrange(1,30):
        f =  open('../data/trump/{0}.txt'.format(i),'rb')
        text = f.read()
        #temp = {'candidate':'trump','date':'0','text':text}
        row = ['trump','0',text]
        csvwriter.writerow(row)

if __name__ == '__main__':
    seed_urls = dict(clinton = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=70&campaign=2016CLINTON&doctype=5000',
    sanders = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=107&campaign=2016SANDERS&doctype=5000',
    #trump = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=115&campaign=2016TRUMP&doctype=5000',
    martin = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=112&campaign=2016OMALLEY&doctype=5000',
    #chafee = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=113&campaign=2016CHAFEE&doctype=5000',
    ted_cruz = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=103&campaign=2016CRUZ&doctype=5000',
    robio = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=105&campaign=2016RUBIO&doctype=5000',
    kasich = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=105&campaign=2016RUBIO&doctype=5000',
    bush = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=101&campaign=2016BUSH&doctype=5000',
    #webb = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=118&campaign=2016WEBB&doctype=5000',
    carson = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=108&campaign=2016CARSON&doctype=5000',
    chris = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=117&campaign=2016CHRISTIE&doctype=5000',
    fiorina = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=106&campaign=2016FIORINA&doctype=5000',
    #rick = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=96&campaign=2016SANTORUM&doctype=5000',
    paul = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=104&campaign=2016PAUL&doctype=5000')
    #mike = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=77&campaign=2016HUCKABEE&doctype=5000',
    #graham = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=110&campaign=2016GRAHAM&doctype=5000',
    #jindal = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=116&campaign=2016JINDAL&doctype=5000',
    #walker = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=109&campaign=2016WALKER&doctype=5000',
    #perry = 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=78&campaign=2016PERRY&doctype=5000')

    #seed_urls = {'clinton':clinton, 'sanders':sanders, 'trump':trump}
    n = 3.
    csvfile =  open(os.path.join(os.path.pardir,'data','speeches_selected.csv'), 'wb')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['candidate','date','text'])
    for candidate, link in seed_urls.iteritems():
        soup = get_soup(link)
        a=soup.find_all('td',class_="listdate")
        l = len(a) #each speach have three tags 1)name, 2)date, 3)link
        a = np.array(a)
        per_speach_records = np.array_split(a,int(l/n))
        for speach_record in per_speach_records:
            row = extract_speach_info(speach_record)
            #print row
            row[0] = candidate
            csvwriter.writerow(row)
    add_trump(csvwriter)
    csvfile.close()

