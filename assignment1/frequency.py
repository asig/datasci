import json
import sys
import regex as re

counts = {}

def remove_punctuation(text):
    return re.sub(ur"\p{P}+", " ", text)

def split_tweet(line):
    line = remove_punctuation(line).lower()
    return line.split()


def main():
    global counts

    # count all the terms
    grand_total = 0
    tweet_file = open(sys.argv[1])
    for line in tweet_file:
        node = json.loads(line)
        text = ''
        if 'text' in node:
            text = node['text']
        tokens = split_tweet(text)
        for token in tokens:
            grand_total += 1
            counts[token] = counts.get(token, 1) + 1

    # dump the frequencies
    for token in counts:
        print token + " " + "%.6f".format(counts[token]/grand_total)


if __name__ == '__main__':
    main()
