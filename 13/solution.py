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

class Cart:
  def __init__(self, ctype, pos, turn):
    self.ctype = ctype
    self.pos = pos
    self.turn = turn

  def update(self, ctype, pos, turn):
    self.ctype = ctype
    self.pos = pos
    self.turn = turn
    return self

  def __repr__(self):
    return "%s" % (self.ctype.value)

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
  return track, Cart(ctype, (i, j), 0)


def print_grid(grid, carts=[]):
  copy = [[c for c in row] for row in grid]
  for c in carts:
    y, x = c.pos
    copy[x][y] = c.ctype
  for row in copy:
    print("".join([str(c.value) for c in row]))


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
  if cart.turn == 0:
    ntype = CartType.RIGHT
  elif cart.turn == 1:
    ntype = cart.ctype
  elif cart.turn == 2:
    ntype = CartType.LEFT
  else:
    raise Exception('Bad turn value %d' % cart.turn)

  cart.update(ntype, npos, (cart.turn + 1) % 3)
  return cart

def update_cart(cart, grid):
  ctype = cart.ctype
  turn = cart.turn
  x, y = cart.pos
  if ctype is CartType.RIGHT:
    rnext = grid[y][x + 1]
    npos = (x + 1, y)
    if rnext is RailType.EW:
      return cart.update(ctype, npos, turn)
    if rnext is RailType.CURVE_UP:
      return cart.update(CartType.UP, npos, turn)
    if rnext is RailType.CURVE_DOWN:
      return cart.update(CartType.DOWN, npos, turn)
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  elif ctype is CartType.LEFT:
    rnext = grid[y][x - 1]
    npos = (x - 1, y)
    if rnext is RailType.EW:
      return cart.update(ctype, npos, turn)
    if rnext is RailType.CURVE_UP:
      return cart.update(CartType.DOWN, npos, turn)
    if rnext is RailType.CURVE_DOWN:
      return cart.update(CartType.UP, npos, turn)
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  elif ctype is CartType.UP:
    rnext = grid[y - 1][x]
    npos = (x, y - 1)
    if rnext is RailType.NS:
      return cart.update(ctype, npos, turn)
    if rnext is RailType.CURVE_UP:
      return cart.update(CartType.RIGHT, npos, turn)
    if rnext is RailType.CURVE_DOWN:
      return cart.update(CartType.LEFT, npos, turn)
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  elif ctype is CartType.DOWN:
    rnext = grid[y + 1][x]
    npos = (x, y + 1)
    if rnext is RailType.NS:
      return cart.update(ctype, npos, turn)
    if rnext is RailType.CURVE_UP:
      return cart.update(CartType.LEFT, npos, turn)
    if rnext is RailType.CURVE_DOWN:
      return cart.update(CartType.RIGHT, npos, turn)
    if rnext is RailType.CROSSING:
      return update_crossing(cart, npos)

  else:
    raise Exception("Don't know how to handle cart, help")

def sort_carts(carts):
  return sorted(carts, key=lambda c: c.pos)

def check_crash(cart, carts):
  for o in carts:
    if o is not cart and o.pos == cart.pos:
      return o.pos
  return False

def step(carts, grid):
  carts = sorted_carts(carts)
  for c in scarts:
    cart = update_cart(c, grid)
  return carts, grid

def run(carts, grid):
  while True:
    # print_grid(grid, carts)
    carts = sort_carts(carts)
    for c in carts:
      cart = update_cart(c, grid)
      crash = check_crash(cart, carts)
      if crash:
        return crash

# grid, carts = parse(open('sample.txt'))
grid, carts = parse(open('input.txt'))
print(carts)
print_grid(grid, carts)

print(run(carts, grid))
# step(*step(*step(carts, grid)))
