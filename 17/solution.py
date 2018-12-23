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
  miny = min([min(clay.y) for clay in clays])
  maxy = max([max(clay.y) for clay in clays])
  minx = min([min(clay.x) for clay in clays]) - 1
  maxx = max([max(clay.x) for clay in clays]) + 1
  grid = {}
  for x in range(minx, maxx):
    for y in range(miny, maxy):
      grid[(x, y)] = '.'

  for vein in clays:


  return grid

def print_grid(grid):
  minx, miny = min(grid.keys())
  maxx, maxy = max(grid.keys())
  for x in range(minx, maxx):
    for y in range(miny, maxy):
      print(grid[(x, y)], end="")
    print()

clays = parse(open('sample.txt'))
print(clays)
print_grid(make_grid(clays))