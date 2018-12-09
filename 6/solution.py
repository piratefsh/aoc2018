import math
def chronal(coords, maxd=30):
  start, end = bounds(coords)
  ex, ey = end
  sx, sy = start

  field = [
    [closest((x, y), coords)
      for x in range(sx, ex + 1)]
        for y in range(sy, ey + 1)]

  width = ex-sx
  height = ey-sy

  border_idx = set([col
    for i, row in enumerate(field)
    for j, col in enumerate(row)
      if i == 0 or
        i == len(field) - 1 or
        j == 0 or
        j == len(row) - 1])

  flat_field = [c for row in field for c in row]
  totals = [flat_field.count(i) for i in range(len(coords))
    if i not in border_idx]

  _, max_cells = max(enumerate(totals), key=lambda x: x[1])
  return max_cells, regions(coords, flat_field, maxd)

def regions(points, flat_field, maxd):
  start, end = bounds(coords)
  ex, ey = end
  sx, sy = start

  reg_size = 0

  for x in range(sx, ex + 1):
    for y in range(sy, ey + 1):
      distances = [man_dist((x,y), pt) for pt in points]
      total_dist = sum(distances)
      if total_dist < maxd:
        reg_size += 1
  return reg_size

def man_dist(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def closest(xy, points):
  distances = [(man_dist(xy, p), i) for i, p in enumerate(points)]
  min_dist, idx = min(distances, key=lambda x: x[0])

  # if has another competing point
  if len([d for d, i in distances if d == min_dist]) > 1:
    return -1
  else:
    return idx

def parse(file):
  return [tuple(map(int, coord.split(', '))) for coord in file]

def bounds(coords):
  min_x, _ = min(coords, key=lambda xy : xy[0])
  _, min_y = min(coords, key=lambda xy : xy[1])

  max_x, _ = max(coords, key=lambda xy : xy[0])
  _, max_y = max(coords, key=lambda xy : xy[1])
  return (min_x, min_y), (max_x, max_y)

def is_finite(coord, others):
  # an area is finite if it is bounded by 4 other points
  pass

coords = parse(open('sample.txt'))
# coords = parse(open('input.txt'))
print(bounds(coords))
print(chronal(coords, 32))
assert(bounds(coords) == ((1, 1), (8, 9)))
assert(chronal(coords, 32) == (17, 16))
print('tests pass')