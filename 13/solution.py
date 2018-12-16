from enum import Enum

class Carts(Enum):
  LEFT ='<'
  RIGHT ='>'
  DOWN = 'v'
  UP = '^'

def cart_state(char, i, j):
  if char == '>':
    ctype = Carts.RIGHT
  elif char == '<':
    ctype = Carts.LEFT
  elif char == '^':
    ctype = Carts.UP
  elif char == 'v':
    ctype = Carts.DOWN
  else:
    raise Error('Unknown cart type: %s' % char)

  track = '-' if ctype is Carts.LEFT or ctype is Carts.RIGHT else '|'
  return track, (char, (i, j))

def print_grid(grid):
  for line in grid:
    print("".join(line))

def parse(file):
  lines = [line[0:-1] for line in file if line]
  width = len(lines[0])

  grid = [[' '] * width for _ in lines]
  carts = []
  for i in range(len(lines)):
    for j in range(len(lines[i])):
      char = lines[i][j]
      if char in "<>v^":
        track, cart = cart_state(char, i, j)
        grid[i][j] = track
        carts.append(cart)
      else:
        grid[i][j] = char
  return grid, carts

grid, carts = parse(open('sample.txt'))
print_grid(grid)