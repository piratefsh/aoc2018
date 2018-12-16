from enum import Enum

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
  def __repr__(self):
    if self.occupant is None:
      return str(self.type.value)

    return(self.occupant.type.value)

class Sprite(Entity):
  def __init__(self, stype, pos):
    Entity.__init__(self, stype);
    self.pos = pos
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
  pass

def turn(curr, sprites, grid):
  #  find all targets
  targets = [s for s in sprites if s.type is not curr.type]

  # find open_squares in range of targets
    # for t in target
      # find N, S, E, W squares
      # if sq is not occupied or wall
      # is open
  for t in target:
    t

  # find in_range_targets

  # if no open_squares or no in_range_targets
    # end turn

  # if has in_range_target,
    # attack

  # else move

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