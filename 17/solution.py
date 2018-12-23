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

    pass

  return grid

def print_grid(grid):
  minx, miny = grid['dims']['min']
  maxx, maxy = grid['dims']['max']
  print('dimensions', minx, maxx, miny , maxy)
  for y in range(miny, maxy):
    for x in range(minx, maxx):
      print(grid[(x, y)], end="")
    print()

clays = parse(open('sample.txt'))
print(clays)
print_grid(make_grid(clays))