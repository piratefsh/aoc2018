from enum import Enum
import math

class CellType(Enum):
  WALL = '#'
  NONE = '.'

class SpriteType(Enum):
  GOBLIN = 'G'
  ELF = 'E'

class Entity:
  def __init__(self, etype, pos, occupant=None):
    self.pos = pos
    self.type = etype
    self.occupant = occupant
    self.visited = False

  def is_open(self):
    return self.type is not CellType.WALL and self.occupant is None

  def is_not_wall(self):
    return self.type is not CellType.WALL

  def remove_occupant(self):
    self.occupant = None

  def add_occupant(self, sprite):
    self.occupant = sprite

  def __repr__(self):
    x, y = self.pos
    return "%s (%d, %d)" % (self.__str__(), x, y)

  def __str__(self):
    if self.occupant is None:
      return str(self.type.value)

    return(self.occupant.type.value)

class Sprite(Entity):
  def __init__(self, stype, pos):
    Entity.__init__(self, stype, pos);
    self.ap = 3
    self.hp = 200
    self.dead = False

  def reduce_hp(self, hp):
    self.hp -= hp
    if self.hp <= 0:
      self.dead = True

  def attack(self, other):
    other.reduce_hp(self.ap)

def parse(file):
  sprites = []
  grid = []
  for y, yrow in enumerate(file):
    row = []
    for x, c in enumerate(yrow.strip()):
      if c == '#':
        row.append(Entity(CellType.WALL, (x, y), None))
      elif c == '.':
        row.append(Entity(CellType.NONE, (x, y), None))
      elif c == 'G':
        sprite = Sprite(SpriteType.GOBLIN, (x, y))
        row.append(Entity(CellType.NONE, (x, y), sprite))
        sprites.append(sprite)
      elif c == 'E':
        sprite = Sprite(SpriteType.ELF, (x, y))
        row.append(Entity(CellType.NONE, (x, y), sprite))
        sprites.append(sprite)
      else:
        raise Exception('Unknown entity %s' % c)
    grid.append(row)
  return grid, sprites

def sort(entities):
  return sorted(entities, key=lambda x: (x.pos[1], x.pos[0]))

def bfs(start, grid, targets):
  queue = [(start, 0)]
  found = dict()
  while len(queue) > 0 and len(targets) > 0:
    curr, dist = queue.pop(0)
    curr.visited = True

    if curr in targets:
      targets.remove(curr)
      found[curr] = dist if not curr in found or dist < found[curr] else dist

    # add neighbours
    x, y = curr.pos
    neighbours = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
    queue += [(grid[y][x], dist+1) for x, y in neighbours
      if y < len(grid) and x < len(grid[0]) and
        grid[y][x].is_not_wall() and
         not grid[y][x].visited and
         not grid[y][x] in queue]

  #  unmark all visited
  for row in grid:
    for col in row:
      col.visited = False

  return found

def neartest_reachable(reachable):
  sreach = sorted(reachable.keys(), key=lambda x: reachable[x])
  nearest_key = sreach[0]
  nearest_dist = reachable[nearest_key]

  # find other nearest
  other_nearest = [k for k in reachable.keys() if reachable[k] == nearest_dist]
  return sort(other_nearest)[0]

def best_move(sprite, grid, open_squares):
  # find shortest distance to each open square
    # do bfs to find all squares it can reach
  reachable = bfs(sprite, grid, open_squares)
  if len(reachable.keys()) < 1:
    return False

  nearest = neartest_reachable(reachable)

  # for all surroundings, find one with nearest manhattan distance
  x, y = sprite.pos
  surroundings = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
  surrounding_dists = {}
  for x, y in surroundings:
    cell = grid[y][x]
    surrounding_dists[cell] = mdist(cell.pos, nearest.pos)

  nearest_next_move = neartest_reachable(surrounding_dists)
  # breakpoint()
  return nearest_next_move

def find_open(curr, grid):
  x, y = curr.pos
  # find N, S, E, W squares
  surroundings = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]

  return [grid[j][i] for i, j in surroundings if grid[j][i].is_open()]

# manhattan distance
def mdist(a, b):
  x1, y1 = a
  x2, y2 = b
  return abs(x2-x1) + abs(y2-y1)

def turn(curr, sprites, grid):
  #  find all targets
  targets = [s for s in sprites if s.type is not curr.type]

  # find open_squares in range of targets
  open_squares = []
  for t in targets:
    open_squares += find_open(t, grid)

  # find in_range_targets, i.e. targets one step away
  in_range_targets = [t for t in targets if mdist(t.pos, curr.pos) <= 1]

  # print(curr, curr.pos, targets)
  # print('open_squares', open_squares)

  if len(open_squares) < 1 and len(in_range_targets) < 1:
    # print('no move')
    # end turn
    return False

  # if has in_range_target
  if len(in_range_targets) > 0:
    # attack target with lowest hp in reading order sort
    target = sorted(sort(in_range_targets), key=lambda x: x.hp)
    # print('in range targets', target)
    curr.attack(target)
    return True
  else:
    # move
    x, y = curr.pos
    best_cell = best_move(grid[y][x], grid, open_squares)

    # print('best move', best_cell.pos)
    if best_cell:
      move_to(curr, best_cell)
      return True

  # print('no move!')
  return False

def move_to(sprite, cell):
  x, y = sprite.pos
  sprite.pos = cell.pos
  cell.add_occupant(sprite)
  grid[y][x].remove_occupant()

def remove_from(s, grid):
  x, y = s.pos
  grid[y][x].remove_occupant()

def print_grid(grid):
  print('  ', end="")
  for x in range(len(grid[0])):
    print(x, end="")
  print()
  for i, row in enumerate(grid):
    print(i, end=" ")
    for col in row:
      print(col, end="")
    print()

def update(grid, sprites):
  has_move = False
  for s in sprites:
    res = turn(s, sprites, grid)
    has_move = has_move or res

    dead = [s for s in sprites if s.dead]
    for d in dead:
      remove_from(s, grid)
      sprites.remove(d)

  return has_move

def run(grid, sprites, steps = 4):
  has_move = True

  while steps > 0:
    steps -= 1
    print_grid(grid)
    has_move = update(grid, sprites)


grid, sprites = parse(open('input.txt'))
grid, sprites = parse(open('sample1.txt'))
print_grid(grid)
run(grid, sprites)
# print(bfs(grid[1][1], grid, [grid[1][4], grid[4][5]]))