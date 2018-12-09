def alt_chronal(beacons, maxd=32):
  start, end = bounds(beacons)
  ex, ey = end
  sx, sy = start

  border_beacons = set()
  cell_counts = [0] * len(beacons)
  total_regions = 0

  for x in range(sx, ex + 1):
    for y in range(sy, ey + 1):
      closest = (0, 10000000)
      dupe = False

      # keep track of total distances to all beacons
      total_dist = 0

      for i, b in enumerate(beacons):
        dist = man_dist((x, y), b)
        total_dist += dist
        cidx, cdist = closest

        if dist < cdist:
          closest = (i, dist)
          dupe = False

        if dist == cdist:
          dupe = True

      cidx, _ = closest

      if x == sx or x == ex or y == sy or y == ey:
        # identify if beacon is at borders
        # and invalidate count if so
        cell_counts[cidx] -= 100000000
      elif not dupe:
        # add closest beacon if there wasn't a duplicate
        cell_counts[cidx] += 1

      # determine if xy is in region
      if total_dist < maxd:
        total_regions += 1

  # ignore beacons that are at borders
  return max(cell_counts), total_regions

def man_dist(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def parse(file):
  return [tuple(map(int, coord.split(', '))) for coord in file]

def bounds(coords):
  min_x, _ = min(coords, key=lambda xy : xy[0])
  _, min_y = min(coords, key=lambda xy : xy[1])

  max_x, _ = max(coords, key=lambda xy : xy[0])
  _, max_y = max(coords, key=lambda xy : xy[1])
  return (min_x, min_y), (max_x, max_y)

coords = parse(open('sample.txt'))
big_coords = parse(open('input.txt'))
assert(alt_chronal(coords, 32) == (17, 16))
assert(alt_chronal(big_coords, 10000) == (2906, 50530))
print('tests pass')