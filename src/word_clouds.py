#!/usr/bin/env python2
"""
python word_clouds.py -c ./data/custom_exclude.txt ../results/most_common_words.txt ../plots/word_clouds/ > ../results/most_common_words_with_count_by_candidates.txt
"""

from wordcloud import WordCloud
from nltk.corpus import stopwords
import os
import argparse
import operator
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="")
parser.add_argument("most_common",
                    help="write list of most common words here")
parser.add_argument("clouds_dir",
                    help="write the clouds in this dir")
parser.add_argument("-c" , "--custom_exclude", dest="custom_exclude", default='',
                    help="custom list of words to exclude")
args = parser.parse_args()


candidates = ['clinton', 'sanders', 'martin', 'ted_cruz', 'rubio', 'kasich', 'bush',
              'carson', 'chris', 'fiorina', 'paul', 'trump']

def print_word_counts(candidate, word_counts, num_top):
  print 'Most common words for ' + candidate + ':'
  sorted_words = sorted(word_counts, key=operator.itemgetter(1), reverse=True)
  most_common = list()
  for i in range(min(num_top, len(sorted_words))):
    print '{}: {}'.format(sorted_words[i][0], sorted_words[i][1])
    most_common.append(sorted_words[i][0])
  print '*************************'
  return most_common



def main():
  exclude = stopwords.words('english')
  if args.custom_exclude:
    with open(args.custom_exclude) as f:
      extra_words_exclude = f.read().splitlines()
    exclude.extend(extra_words_exclude)

  exclude = set(exclude)
  most_common_words_of_all_candidates = set()
  for candidate in candidates:
    # add candidate herself to exclude and at the end remove
    exclude.add(candidate)
    input_directory = os.path.join(os.path.pardir, 'data', candidate)
    input_file = os.path.join(input_directory, 'all_speeches.txt')

    # Read the whole text.
    text = open(input_file).read().lower()

    # Generate a word cloud image
    wordcloud = WordCloud(width=1000, height=600, stopwords=exclude).generate(text)
    wordcounts = WordCloud(stopwords=exclude).process_text(text)
    most_common = print_word_counts(candidate, wordcounts, 60)
    most_common_words_of_all_candidates = most_common_words_of_all_candidates.union(most_common)

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud)
    plt.axis("off")
    output_file = os.path.join(args.clouds_dir, candidate + '_words_cloud.pdf')
    plt.savefig(output_file)

    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(width=1000, height=600, max_font_size=40, relative_scaling=.5,
                          stopwords=exclude).generate(text)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    output_file = os.path.join(args.clouds_dir, candidate + '_words_cloud_scaled.pdf')
    plt.savefig(output_file)
    #plt.show()
    # remove candiate herself from exclude list before we moved to other candidates
    exclude.remove(candidate)

  with open(args.most_common, "w") as myfile:
    for word in most_common_words_of_all_candidates:
      myfile.write("%s\n" % word)


if __name__ == '__main__':
  main()
