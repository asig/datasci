import json
import sys
import unicodedata

counts = {}

def remove_punctuation(text):
    punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
    return ''.join(x for x in text
                   if unicodedata.category(x) not in punctutation_cats)

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
            counts[token] = counts.get(token, 0) + 1

    # dump the frequencies
    for token in counts:
        print "%s %.12f" % (token.encode('utf-8'), float(counts[token])/float(grand_total))


if __name__ == '__main__':
    main()
