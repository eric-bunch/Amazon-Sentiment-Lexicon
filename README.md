This script will build a sentiment lexicon analgous to the AFINN setniment lexicon, based on 
Amazon customer reviews. The Amazon customer reviews were obtained from the SNAP group 
(http://snap.stanford.edu/). Before the script build_amazon_sentiment_lexicon.py is run, 
the reviews are normalized with the script normalize_reviews.py. The normalize script takes 
all the reviews for a certain genre, and splits them into three groups: one to build the sentiment 
lexicon from, one to train some machine learning algorithms on, and one to test the machine learning 
algorithms on. Also, each of these three groups will have the same number of reviews of score 
1, 2, 3, 4, and 5. 

The script that builds the sentiment lexicon reads through the reviews that the normalization script 
set aside for it. As it does this, the scrip counts how many times each word appears in a review of 
score 1, 2, 3, 4, or 5. Then after the script is done reading, each word is assigned the score (1 through 5) 
for which it had the most occurences in. It then writes out this lexicon to a file. The results of 
this process for the Automotive genre are given in this project.
