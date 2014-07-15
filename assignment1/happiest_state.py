import math
import json
import sys
import unicodedata

scores = {}
states = {'AK':1,
'AL':1,
'AR':1,
'AZ':1,
'CA':1,
'CO':1,
'CT':1,
'DC':1,
'DE':1,
'FL':1,
'GA':1,
'HI':1,
'IA':1,
'ID':1,
'IL':1,
'IN':1,
'KS':1,
'KY':1,
'LA':1,
'MA':1,
'MD':1,
'ME':1,
'MI':1,
'MN':1,
'MO':1,
'MS':1,
'MT':1,
'NC':1,
'ND':1,
'NE':1,
'NH':1,
'NJ':1,
'NM':1,
'NV':1,
'NY':1,
'OH':1,
'OK':1,
'OR':1,
'PA':1,
'RI':1,
'SC':1,
'SD':1,
'TN':1,
'TX':1,
'UT':1,
'VA':1,
'VT':1,
'WA':1,
'WI':1,
'WV':1,
'WY':1}

# Haversine distance formula, taken from http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
# Author: Wayne Dyck
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

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


def tweet_state(tweetJson):
    node = json.loads(tweetJson)
    coordinates = node.get('coordinates', None)
    if coordinates != None:
        coordinates = coordinates.get('coordinates', None)
        if coordinates != None:
            # print "%.6f %.6f" % (coordinates[0], coordinates[1])
            return None
    place = node.get('place', None)
    if place != None:
        country_code = place.get('country_code')
        if country_code == "US":
            full_name = place.get('full_name')
            state = full_name.split(",")[1].strip()
            if states.has_key(state):
                return state

    return  None



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

    state_score = {}
    state_cnt = {}
    for line in tweet_file:
        score = tweet_sentiment(line)
        state = tweet_state(line)
        if state != None:
            state_cnt[state] = state_cnt.get(state, 0) + 1
            state_score[state] = state_score.get(state, 0) + score

    # Find max average score
    max_score = -1000
    max_state = ''
    for state in state_score.keys():
        score = float(state_score[state]) / state_cnt[state]
        if score > max_score:
            max_score = score
            max_state = state
    print max_state
    # print max_score
    # print state_cnt[max_state], state_score[max_state]


if __name__ == '__main__':
    main()
