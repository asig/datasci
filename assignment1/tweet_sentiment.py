import json
import sys
import regex as re

scores = {}

def load_scores(f):
    global scores
    scores = {}
    for line in f:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        uterm = unicode(term, "utf-8")
        scores[uterm] = int(score)  # Convert the score to an integer.


def remove_punctuation(text):
    return re.sub(ur"\p{P}+", " ", text)

def compute_score(line):
    line = remove_punctuation(line).lower()
    score = 0
    for term in line.split():
        if term in scores:
            score += scores[term]
    return score


def main():
    sentiment_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    load_scores(sentiment_file)

    for line in tweet_file:
        node = json.loads(line)
        text = ''
        if 'text' in node:
            text = node['text']
        score = compute_score(text)
        print score


if __name__ == '__main__':
    main()
