import MapReduce
import sys

"""
Unique trims
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    seqid = record[0]
    nucleotids = record[1]
    mr.emit_intermediate(nucleotids[:-10], 1)

def reducer(key, list_of_values):
    # key: shortened nucleotid
    # list_of_values: how often we've seen it. ignored
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
