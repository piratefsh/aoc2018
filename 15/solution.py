from enum import Enum

class CellType(Enum):
  WALL = '#'
  NONE = '.'

class SpriteType(Enum):
  GOBLIN = 'G'
  ELF = 'E'

class Entity:
  def __init__(self, etype):
    self.type = etype
  def __repr__(self):
    return str(self.type.value)

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
        row.append(Entity(CellType.NONE))
        sprites.append(Sprite(SpriteType.GOBLIN, (x, y)))
      elif c == 'E':
        row.append(Entity(CellType.NONE))
        sprites.append(Sprite(SpriteType.ELF, (x, y)))
      else:
        raise Exception('Unknown entity %s' % c)
    grid.append(row)
  return grid, sprites

def print_grid(grid, sprites):
  copy = [[c for c in row ]for row in grid]
  for s in sprites:
    x, y = s.pos
    copy[y][x] = s

  for row in copy:
    for col in row:
      print(col, end="")
    print()

grid, sprites = parse(open('sample1.txt'))
print_grid(grid, sprites)