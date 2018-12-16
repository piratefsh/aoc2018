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
  return track, (ctype, (i, j), 0)


def print_grid(grid, carts=[]):
  copy = [[c for c in row] for row in grid]
  for c in carts:
    ctype, pos, _ = c
    y, x = pos
    copy[x][y] = ctype
  for row in copy:
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
        track, cart = cart_state(char, j, i)
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

def update_crossing(cart, npos):
  ctype, pos, turn = cart
  if turn == 0:
    ntype = CartType.RIGHT
  elif turn == 1:
    ntype = ctype
  elif turn == 2:
    ntype = CartType.LEFT
  else:
    raise Exception('Bad turn value %d' % turn)
  return ntype, npos, (turn + 1) % 3

def update_cart(cart, grid):
  ctype, pos, turn = cart
  x, y = pos
  if ctype is CartType.RIGHT:
    rnext = grid[y][x + 1]
    npos = (x + 1, y)
    if rnext is RailType.EW:
      return ctype, npos, turn
    if rnext is RailType.CURVE_UP:
      return CartType.UP, npos, turn
    if rnext is RailType.CURVE_DOWN:
      return CartType.DOWN, npos, turn
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  elif ctype is CartType.LEFT:
    rnext = grid[y][x - 1]
    npos = (x - 1, y)
    if rnext is RailType.EW:
      return ctype, npos, turn
    if rnext is RailType.CURVE_UP:
      return CartType.DOWN, npos, turn
    if rnext is RailType.CURVE_DOWN:
      return CartType.UP, npos, turn
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  elif ctype is CartType.UP:
    rnext = grid[y - 1][x]
    npos = (x, y - 1)
    if rnext is RailType.NS:
      return ctype, npos, turn
    if rnext is RailType.CURVE_UP:
      return CartType.RIGHT, npos, turn
    if rnext is RailType.CURVE_DOWN:
      return CartType.LEFT, npos, turn
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  elif ctype is CartType.DOWN:
    rnext = grid[y + 1][x]
    npos = (x, y + 1)
    if rnext is RailType.NS:
      return ctype, npos, turn
    if rnext is RailType.CURVE_UP:
      return CartType.LEFT, npos, turn
    if rnext is RailType.CURVE_DOWN:
      return CartType.RIGHT, npos, turn
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  else:
    raise Exception("Don't know how to handle cart, help")

def sort_carts(carts):
  return sorted(carts, key=lambda c: c[1])

def check_crash(cart, carts):
  for other in carts:
    _, opos, _ = other
    _, cpos, _ = cart

    if opos == cpos:
      return opos
  return False

def step(carts, grid):
  updated_carts = []
  for c in sort_carts(carts):
    cart = update_cart(c, grid)
    if cart:
      updated_carts.append(cart)
  carts = updated_carts
  return carts, grid

def run(carts, grid):
  while True:
    updated_carts = []

    for c in sort_carts(carts):
      cart = update_cart(c, grid)
      if cart:
        crash = check_crash(cart, updated_carts)
        if crash:
          return crash
        updated_carts.append(cart)
    carts = updated_carts
    # print_grid(grid, carts)

# grid, carts = parse(open('sample.txt'))
grid, carts = parse(open('input.txt'))
print(carts)
print_grid(grid, carts)

print(run(carts, grid))
# step(*step(*step(carts, grid)))
