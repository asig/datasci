import json
import sys
import operator


def main():
    counts = {}
    tweet_file = open(sys.argv[1])

    grand_total = 0
    for line in tweet_file:
        node = json.loads(line)
        if 'entities' in node:
            node = node['entities']
            if 'hashtags' in node:
                node = node['hashtags']
                for tag in node:
                    tagtext = tag['text']
                    grand_total += 1
                    counts[tagtext] = counts.get(tagtext, 0) + 1

    sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
    for i in range(1, 10):
        print "%s %.6f" % (sorted_counts[i][0].encode("utf-8"), float(sorted_counts[i][1])/grand_total)



if __name__ == '__main__':
    main()
