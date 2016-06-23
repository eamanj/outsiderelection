import sys
import os

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pylab as plt
import collections


def main():
  df = pd.read_csv(os.path.join(os.path.pardir,'data','speeches.csv'))
  all_speeches = collections.defaultdict(list)
  for index, row in df.iterrows():
    candidate = row['candidate']
    text = row['text']
    all_speeches[candidate].append(text)

  for candidate, speeches in all_speeches.iteritems():
    directory = os.path.join(os.path.pardir, 'data', candidate)
    if not os.path.isdir(directory):
      os.makedirs(directory)
    with open(os.path.join(directory, 'all_speeches.txt'), "w") as myfile:
      for speech in speeches:
        myfile.write("%s\n" % speech)

if __name__ == '__main__':
  main()
