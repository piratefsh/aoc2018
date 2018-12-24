from collections import namedtuple
import re
import sys
sys.setrecursionlimit(2**16)
Clay = namedtuple('Clay', "x, y")

def parse_coord(cstr, var):
  pattern = re.compile(var + '=([0-9.]*)')
  coord = re.match(pattern, cstr).groups()[0]
  ranges = [int(c) for c in coord.split('..')]
  if len(ranges) == 1:
    return ranges * 2
  return ranges

def parse(file):
  clay = []
  for line in file:
    sx, sy = sorted(line.strip().split(', '))
    x = parse_coord(sx, 'x')
    y = parse_coord(sy, 'y')
    clay.append(Clay(x, y))
  return clay

def make_grid(clays):
  miny = min([min(clay.y) for clay in clays]) - 1
  maxy = max([max(clay.y) for clay in clays]) + 1
  minx = min([min(clay.x) for clay in clays]) - 1
  maxx = max([max(clay.x) for clay in clays]) + 1

  grid = {}

  for x in range(minx, maxx):
    for y in range(miny, maxy):
      grid[(x, y)] = '.'

  grid['dims'] = {
    'min': (minx, miny),
    'max': (maxx, maxy)
  }

  for sex, sey in clays:
    sx, ex = sex
    sy, ey = sey
    for x in range(sx, ex + 1):
      for y in range(sy, ey + 1):
        grid[(x, y)] = '#'
  return grid

def print_grid(grid):
  minx, miny, maxx, maxy = get_dims(grid)
  # print('dimensions', minx, maxx, miny , maxy)
  for y in range(miny, maxy):
    for x in range(minx, maxx):
      print(grid[(x, y)], end="")
    print()
  print()

def get_dims(grid):
  minx, miny = grid['dims']['min']
  maxx, maxy = grid['dims']['max']
  return minx, miny, maxx, maxy

def is_bottom(cell):
  return cell == '#' or cell == '~'

def is_flowing(cell):
  return cell == '|'

def is_water(cell):
  return cell == '~' or cell == '|'

def count_water(grid):
  minx, miny, maxx, maxy = get_dims(grid)
  counter = 0
  for x in range(minx, maxx):
    for y in range(miny + 1, maxy):
      cell = grid[(x, y)]
      if is_water(cell):
        counter += 1
  return counter

def flow(grid, curr=(500, 0)):
  minx, miny, maxx, maxy = get_dims(grid)
  x, y = curr
  curr_cell = grid[(x, y)]

  # if reached the max y
  if y < miny or y >= maxy - 1 or x >= maxx or x < 0:
    grid[(x, y)] = '|'
    return None

  # if has hit an edge
  if is_bottom(curr_cell):
    return (x, y)

  if is_flowing(curr_cell):
    return None

  # if has bottom (still water or clay)
  if is_bottom(grid[(x, y + 1)]):
    grid[(x, y)] = '|'
    # flood to left
    lbound = flow(grid, (x-1, y))
    # flood to right
    rbound = flow(grid, (x+1, y))

    # if had clay bounds
    if lbound and rbound:
      lx, ly = lbound
      rx, ry = rbound

      if(ly == ry):
        # replace entire level with still water
        for nx in range(lx+1, rx):
          grid[(nx, ly)] = '~'

      # pop up and flow
      grid[(x, y-1)] = '.'
      return flow(grid, (x, y-1))
    else:
      return lbound or rbound
  # else flood down
  else:
    grid[(x, y)] = '|'
    return flow(grid, (x, y+1))


# clays = parse(open('sample.txt'))
clays = parse(open('input.txt'))
grid = make_grid(clays)
# print_grid(grid)
print(get_dims(grid))
minx, miny, maxx, maxy = get_dims(grid)
print(flow(grid, (500, miny)))
print_grid(grid)
print(count_water(grid))