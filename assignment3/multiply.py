import MapReduce
import sys

"""
Matrix Multiplication
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    matrix, i, j, value = record
    if matrix == "a":
        # emit i,0 .. i,k
        for k in range(0, 5):
            mr.emit_intermediate( (i, k), (j, "a", value))
    else:
        # emit 0,j .. k,j
        for k in range(0, 5):
            mr.emit_intermediate( (k,j), (i, "b", value))

def reducer(key, list_of_values):
    # mr.emit( (key, list_of_values) )
    a = {}
    b = {}
    for idx in range(0, 5):
        a[idx] = 0
        b[idx] = 0
    for v in list_of_values:
        idx = v[0]
        if v[1] == "a":
            a[idx] = v[2]
        else:
            b[idx] = v[2]
    total = 0
    for idx in range(0, 5):
        total += a[idx] * b[idx]
    mr.emit((key[0], key[1], total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
