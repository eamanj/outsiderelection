python word_clouds.py -c ./data/custom_exclude.txt ../data ../results/most_common_words.txt ../plots/word_clouds/ > ../results/most_common_words_with_count_by_candidates.txt

python tfidf.py -c ./data/custom_exclude.txt ../results/most_common_words.txt

python word_clouds.py -c ./data/custom_exclude.txt ../data/tfidf/ ../tmp ../plots/tfids_wordclouds/
