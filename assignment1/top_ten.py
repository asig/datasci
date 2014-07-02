import json
import sys
import operator
counts = {}



def main():
    global counts
    tweet_file = open(sys.argv[1])

    for line in tweet_file:
        node = json.loads(line)
        if 'entities' in node:
            node = node['entities']
            if 'hashtags' in node:
                node = node['hashtags']
                for tag in node:
                    tagtext = tag['text']
                    counts[tagtext] = counts.get(tagtext, 0) + 1

    sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
    for i in range(1, 10):
        print sorted_counts[i]



if __name__ == '__main__':
    main()
