import MapReduce
import sys

"""
Join
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    id = record[1]
    mr.emit_intermediate(id, record)

def reducer(key, list_of_values):
    orders = []
    items = []
    for v in list_of_values:
        type = v[0]
        if type == "order":
            orders.append(v)
        else:
            items.append(v)
    for order in orders:
        for item in items:
            mr.emit( order + item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
