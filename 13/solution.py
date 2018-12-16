from enum import Enum
import re


class CartType(Enum):
  LEFT = '<'
  RIGHT = '>'
  DOWN = 'v'
  UP = '^'


class RailType(Enum):
  EW = '-'
  NS = '|'
  CURVE_UP = '/'
  CURVE_DOWN = '\\'
  NONE = ' '
  CROSSING = '+'


def cart_state(char, i, j):
  if char == '>':
    ctype = CartType.RIGHT
  elif char == '<':
    ctype = CartType.LEFT
  elif char == '^':
    ctype = CartType.UP
  elif char == 'v':
    ctype = CartType.DOWN
  else:
    raise Exception('Unknown cart type: %s' % char)

  track = RailType.EW if ctype is CartType.LEFT or ctype is CartType.RIGHT else RailType.NS
  return track, (ctype, (i, j))


def print_grid(grid):
  for row in grid:
    print("".join([c.value for c in row]))


def parse(file):
  lines = [line[0:-1] for line in file if line]
  width = len(lines[0])

  grid = [[RailType.NONE] * width for _ in lines]
  carts = []
  for i in range(len(lines)):
    for j in range(len(lines[i])):
      char = lines[i][j]
      if char in "<>v^":
        track, cart = cart_state(char, i, j)
        grid[i][j] = track
        carts.append(cart)
      else:
        if char == ' ':
          rtype = RailType.NONE
        elif char == '-':
          rtype = RailType.EW
        elif char == '|':
          rtype = RailType.NS
        elif char == '/':
          rtype = RailType.CURVE_UP
        elif char == '\\':
          rtype = RailType.CURVE_DOWN
        elif char == '+':
          rtype = RailType.CROSSING
        else:
          raise Exception('Unknown rail type: %s' % char)

        grid[i][j] = rtype
  return grid, carts

def update_crossing(cart, grid):
  return cart
def update_cart(cart, grid):
  ctype, pos = cart
  x, y = pos
  if ctype is CartType.RIGHT:
    rnext = grid[x][y + 1]
    npos = (x, y + 1)
    if rnext is RailType.EW:
      return ctype, npos
    if rnext is RailType.CURVE_UP:
      return CartType.UP, npos
    if rnext is RailType.CURVE_DOWN:
      return CartType.DOWN, npos
    if rnext is RailType.CROSSING:
      return update_crossing(cart, grid)

  elif ctype is CartType.LEFT:
    rnext = grid[x][y - 1]
    npos = (x, y - 1)
    if rnext is RailType.EW:
      return ctype, npos
    if rnext is RailType.CURVE_UP:
      return CartType.DOWN, npos
    if rnext is RailType.CURVE_DOWN:
      return CartType.UP, npos
    if rnext is RailType.CROSSING:
      return update_crossing(cart, grid)

  elif ctype is CartType.UP:
    rnext = grid[x - 1][y]
    npos = (x - 1, y)
    if rnext is RailType.NS:
      return ctype, npos
    if rnext is RailType.CURVE_UP:
      return CartType.RIGHT, npos
    if rnext is RailType.CURVE_DOWN:
      return CartType.LEFT, npos
    if rnext is RailType.CROSSING:
      return update_crossing(cart, grid)

  elif ctype is CartType.DOWN:
    rnext = grid[x + 1][y]
    npos = (x + 1, y)
    if rnext is RailType.NS:
      return ctype, npos
    if rnext is RailType.CURVE_UP:
      return CartType.LEFT, npos
    if rnext is RailType.CURVE_DOWN:
      return CartType.RIGHT, npos
    if rnext is RailType.CROSSING:
      return update_crossing(cart, grid)

  raise Exception("Unknown cart, help")

def sort_carts(carts):
  return sorted(carts, key=lambda c: c[1])


def step(carts, grid):
  updated_carts = []

  for c in sort_carts(carts):
    cart = update_cart(c, grid)
    if cart:
      updated_carts.append(cart)
  carts = updated_carts

  print(carts)
  return carts, grid


grid, carts = parse(open('sample.txt'))
# grid, carts = parse(open('input.txt'))
print_grid(grid)
step(*step(*step(carts, grid)))
