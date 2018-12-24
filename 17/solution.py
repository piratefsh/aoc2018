from collections import namedtuple
import re

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

def get_dims(grid):
  minx, miny = grid['dims']['min']
  maxx, maxy = grid['dims']['max']
  return minx, miny, maxx, maxy

def is_bottom(cell):
  return cell == '#' or cell == '~'

def is_occupied(cell):
  return is_bottom(cell) or cell == '|'

def flow(grid, curr=(500, 0)):
  print_grid(grid)
  minx, miny, maxx, maxy = get_dims(grid)
  x, y = curr
  curr_cell = grid[(x, y)]
  # if reached the max y
  if y < miny or y >= maxy -1 or x >= maxx - 1 or x < 0:
    return None

  # if has hit an edge
  if is_bottom(curr_cell):
    return (x, y)

  if curr_cell == '|':
    return None

  # if has bottom (still water or clay)
  if is_bottom(grid[(x, y + 1)]):
    grid[(x, y)] = '|'
    # flood to left
    lbound = flow(grid, (x-1, y))
    # flood to right
    rbound = flow(grid, (x+1, y))
    print(x, y, lbound, rbound)
    # if had clay bounds
    if lbound and rbound:
      # replace entire level with still water
      lx, ly = lbound
      rx, ry = rbound
      for nx in range(lx, rx):
        grid[(nx, ly)] = '~'
        print(grid[(nx, ly)])
      # pop up
      # breakpoint()
      grid[(x, y-1)] = '.'
      flow(grid, (x, y-1))
  # else flood down
  else:
    grid[(x, y)] = '|'
    flow(grid, (x, y+1))


clays = parse(open('sample.txt'))
grid = make_grid(clays)
print_grid(grid)
print(flow(grid))
print_grid(grid)