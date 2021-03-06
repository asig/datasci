import json
import sys
import unicodedata

scores = {}

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


def tweet_sentiment(tweetJson):
    node = json.loads(tweetJson)
    text = remove_punctuation(node.get('text', '')).lower()
    score = 0
    for term in text.split():
        if term in scores:
            score += scores[term]
    return score


def main():
    sentiment_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    load_scores(sentiment_file)

    for line in tweet_file:
        score = tweet_sentiment(line)
        print score


if __name__ == '__main__':
    main()
