#!/usr/bin/env python2
"""
python tfidf.py -c ./data/custom_exclude.txt ../results/most_common_words.txt ../results/word_scores.csv
"""

from nltk.corpus import stopwords
import os
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser(description="")
parser.add_argument("vocabulary",
        help="The file of vocabularies for which we will extract tfidf")
parser.add_argument("output_file",
        help="The output file containing word scores")
parser.add_argument("-c" , "--custom_exclude", dest="custom_exclude", default='',
        help="custom list of words to exclude")
parser.add_argument("-m", "--max_df", dest="max_df", type=float, default=0.85)
parser.add_argument("-s", "--sublinear_tf", dest="sublinear_tf", default=False,
        action="store_true")
parser.add_argument("-n", "--norm", dest="norm", default=None, choices=[None, 'l1', 'l2'])
args = parser.parse_args()

candidates = ['clinton', 'sanders', 'martin', 'ted_cruz', 'rubio', 'kasich', 'bush',
        'carson', 'chris', 'fiorina', 'paul', 'trump']

def main():
    # get the list of vocab for which to compute tfidf
  with open(args.vocabulary) as f:
      vocab = f.read().splitlines()
  vocab = set(vocab)

  # get list of stopwords
  exclude = stopwords.words('english')
  if args.custom_exclude:
      with open(args.custom_exclude) as f:
          extra_words_exclude = f.read().splitlines()
    exclude.extend(extra_words_exclude)

  exclude = list(set(exclude))

  vect = TfidfVectorizer(sublinear_tf=args.sublinear_tf,
          max_df=args.max_df,
          analyzer='word', 
          stop_words=exclude,
          vocabulary=vocab,
          norm=args.norm)

  # generate corpus
  corpus = list()
  corpus_docs = list()
  for candidate in candidates:
      directory = os.path.join(os.path.pardir, 'data', candidate)
    for speech_file in os.listdir(directory):
        if speech_file == 'all_speeches.txt':
            continue
      # now we know this is a single speech file
      input_file = os.path.join(directory, speech_file)
      # Read the whole text.
      text = open(input_file).read().lower()
      corpus.append(text)
      corpus_docs.append(candidate + '_' + speech_file)


  corpus_tf_idf = vect.fit_transform(corpus)

if __name__ == '__main__':
    main()
