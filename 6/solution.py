def chronal(coords):

  # sort by y then x coord
  coords.sort(key=lambda xy: xy[1])
  coords.sort(key=lambda xy: xy[0])

  _, size = bounds(coords)
  sizex, sizey = size

  # field = [[0] * sizey for i in range(sizex)]

  field = [closest((x, y), coords)
    for x in range(sizex + 1)
      for y in range(sizey + 1)]

  totals = [field.count(i) for i in range(len(coords))]
  idx, max_cells = max(enumerate(totals), key=lambda x: x[1])
  return max_cells

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

coords = parse(open('input.txt'))
print(bounds(coords))
# assert(bounds(coords) == ((1, 1), (8, 9)))
# assert(chronal(coords) == 17)
print(chronal(coords))
print('tests pass')