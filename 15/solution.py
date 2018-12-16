from enum import Enum
import math

class CellType(Enum):
  WALL = '#'
  NONE = '.'

class SpriteType(Enum):
  GOBLIN = 'G'
  ELF = 'E'

class Entity:
  def __init__(self, etype, occupant=None):
    self.type = etype
    self.occupant = occupant

  def is_open(self):
    return self.type is not CellType.WALL and self.occupant is None

  def __repr__(self):
    if self.occupant is None:
      return str(self.type.value)

    return(self.occupant.type.value)

class Sprite(Entity):
  def __init__(self, stype, pos):
    Entity.__init__(self, stype);
    self.pos = pos

  def attack(self, other):
    # todo
    pass

def parse(file):
  sprites = []
  grid = []
  for y, yrow in enumerate(file):
    row = []
    for x, c in enumerate(yrow.strip()):
      if c == '#':
        row.append(Entity(CellType.WALL))
      elif c == '.':
        row.append(Entity(CellType.NONE))
      elif c == 'G':
        sprite = Sprite(SpriteType.GOBLIN, (x, y))
        row.append(Entity(CellType.NONE, sprite))
        sprites.append(sprite)
      elif c == 'E':
        sprite = Sprite(SpriteType.ELF, (x, y))
        row.append(Entity(CellType.NONE, sprite))
        sprites.append(sprite)
      else:
        raise Exception('Unknown entity %s' % c)
    grid.append(row)
  return grid, sprites

def sort(entities):
  return sorted(entities, key=lambda x: x.pos)

def move(sprite, sprites, grid, open_squares):
  # find distance to each open square

  # sort by distance, then reading order

  # pick nearest
  pass

def find_open(curr, grid):
  x, y = curr.pos
  # find N, S, E, W squares
  surroundings = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]

  return [grid[i][j] for i, j in surroundings if grid[i][j].is_open()]

def dist(a, b):
  x1, y1 = a
  x2, y2 = b
  return math.abs((x2-x1) + (y2-y1))

def turn(curr, sprites, grid):
  #  find all targets
  targets = [s for s in sprites if s.type is not curr.type]

  # find open_squares in range of targets
  open_squares = [find_open(t, grid) for t in target]

  # find in_range_targets, i.e. targets one step away
  in_range_targets = [t for t in targets if dist(s, curr.pos) <= 1]

  if len(open_squares) < 1 and len(in_range_targets) < 1:
    # end turn
    return False

  # if has in_range_target
  if len(in_range_targets) > 0:
    # attack
    target = sort(in_range_targets)[0]
    curr.attack(target)
    return True
  else:
    # move
    move(curr, sprites, grid, open_squares)

def print_grid(grid):
  for row in grid:
    for col in row:
      print(col, end="")
    print()

def run(grid, sprites):
  has_move = True
  while has_move:
    has_move = False
    for s in sprites:
      has_move = has_move or turn(c, sprites, grid)


grid, sprites = parse(open('sample1.txt'))
print_grid(grid)
print(find_open(sprites[0], grid))
print(find_open(sprites[4], grid))
print(find_open(sprites[5], grid))