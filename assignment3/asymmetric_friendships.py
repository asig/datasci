import MapReduce
import sys

"""
Friend Count
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    personA = record[0]
    personB = record[1]
    mr.emit_intermediate((personA, personB), 1) # We've seen this pair
    mr.emit_intermediate((personB, personA), -1) # And we expect to see this one

def reducer(key, list_of_values):
    total = 0
    for v in list_of_values:
        total += v
    if total < 0:
        mr.emit ( key )
        mr.emit ( (key[1], key[0]) )



# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
