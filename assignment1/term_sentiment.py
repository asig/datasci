import json
import sys
import unicodedata

scores = {}
new_terms_positive_tweets = {}
new_terms_negative_tweets = {}
new_terms_all = {}

tweets = {}
tweet_scores = {}

def load_scores(f):
    global scores
    scores = {}
    for line in f:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        uterm = unicode(term, "utf-8")
        scores[uterm] = int(score)  # Convert the score to an integer.


def remove_punctuation(text):
    punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
    return ''.join(x for x in text
                   if unicodedata.category(x) not in punctutation_cats)


def new_terms(node):
    new_terms = {}
    text = remove_punctuation(node.get('text', '')).lower()
    for term in text.split():
        if not term in scores:
            new_terms[term] = 0
    return new_terms


def tweet_sentiment(node):
    text = remove_punctuation(node.get('text', '')).lower()
    score = 0
    for term in text.split():
        if term in scores:
            score += scores[term]
    return score


def main():
    global tweets, tweet_scores,new_terms_positive_tweets, new_terms_negative_tweets,new_terms_all
    sentiment_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    load_scores(sentiment_file)

    # compute scores for each tweet
    i = 0
    for line in tweet_file:
        node = json.loads(line)
        score = tweet_sentiment(node)
        for term in new_terms(node):
            new_terms_all[term] = new_terms_all.get(term, 0) + 1
        if score > 0:
            for term in new_terms(node):
                new_terms_positive_tweets[term] = new_terms_positive_tweets.get(term, 0) + 1
        elif score < 0:
            for term in new_terms(node):
                new_terms_negative_tweets[term] = new_terms_negative_tweets.get(term, 0) + 1


    # compute scores for each new term
    for term in new_terms_all:
        pos = float(new_terms_positive_tweets.get(term,0))
        neg = float(new_terms_negative_tweets.get(term,0))
        if neg == 0:
            neg = 1
        print "%s %.12f" % (term.encode('utf-8'), pos/neg)


if __name__ == '__main__':
    main()
