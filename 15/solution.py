from enum import Enum
import math
import time
DEBUG = False

class NoTargetsException(Exception):
  pass
class ElfDeadException(Exception):
  pass

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

  def copy(self):
    return self.__class__(self.type, (self.pos[0], self.pos[1]))

class Sprite(Entity):
  def __init__(self, stype, pos):
    Entity.__init__(self, stype, pos);
    self.ap = 3
    self.hp = 200
    self.dead = False
    self.raise_exception = False

  def set_ap(self, ap):
    self.ap = ap

  def reduce_hp(self, hp):
    self.hp -= hp
    if self.hp <= 0:
      self.dead = True
      if self.raise_exception and self.type == SpriteType.ELF:
        raise ElfDeadException()

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

# manhattan distance
def mdist(a, b):
  x1, y1 = a
  x2, y2 = b
  return abs(x2-x1) + abs(y2-y1)

def find_open(curr, grid):
  x, y = curr.pos
  # find N, S, E, W squares
  surroundings = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]

  return [grid[j][i] for i, j in surroundings if grid[j][i].is_open()]

def bfs(start, grid, targets):
  queue = [start]
  queue_dist = [0]
  found = dict()
  while len(queue) > 0 and len(targets) > 0:
    # print(len(queue), len(targets), len(grid) * len(grid[0]))
    curr = queue.pop(0)
    dist = queue_dist.pop(0)
    curr.visited = True

    if curr in targets:
      targets.remove(curr)
      found[curr] = dist if not curr in found or dist < found[curr] else dist

    # add neighbours
    neighbours = get_open_neighbours(curr, grid)
    for n in neighbours:
      if not n.visited and not n in queue:
        queue.append(n)
        queue_dist.append(dist + 1)

  #  unmark all visited
  for row in grid:
    for col in row:
      col.visited = False

  return found

def find_min(reachable):
  sreach = sorted(reachable.keys(), key=lambda x: reachable[x])
  nearest_key = sreach[0]
  nearest_dist = reachable[nearest_key]

  # find other nearest
  other_nearest = [k for k in reachable.keys() if reachable[k] == nearest_dist]
  return sort(other_nearest)[0]

def get_open_neighbours(sprite, grid):
  x, y = sprite.pos
  surroundings = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
  return [grid[y][x] for x, y in surroundings if
    y < len(grid) and x < len(grid[0]) and
    grid[y][x].is_open()]

def best_move(sprite, grid, open_squares):
  # find shortest distance to each open square
    # do bfs to find all squares it can reach
  reachable = bfs(sprite, grid, open_squares)
  if len(reachable.keys()) < 1:
    return False

  nearest = find_min(reachable)

  # for all surroundings, find one with nearest manhattan distance
  surroundings = get_open_neighbours(sprite, grid)
  surrounding_dists = {}
  for cell in surroundings:
    reachable = bfs(cell, grid, [nearest])
    if len(reachable.keys()) > 0:
      surrounding_dists[cell] = reachable[nearest]

  nearest_next_move = find_min(surrounding_dists)
  return nearest_next_move


def attempt_attack(curr, targets):
  # find in_range_targets, i.e. targets one step away
  in_range_targets = [t for t in targets if mdist(t.pos, curr.pos) == 1]

  # if has in_range_target
  if len(in_range_targets) > 0:
    # attack target with lowest hp
    target_hps = {}
    for r in in_range_targets:
      target_hps[r] = r.hp
    target = find_min(target_hps)
    curr.attack(target)
    return True
  return False

def turn(curr, sprites, grid):
  if curr.dead:
    return False

  made_move = False
  #  find all targets
  targets = [s for s in sprites if s.type is not curr.type and not s.dead]

  if(len(targets) < 1):
    raise NoTargetsException('game end')

  # find open_squares in range of targets
  open_squares = []
  for t in targets:
    open_squares += find_open(t, grid)

  # try to attack
  made_move = attempt_attack(curr, targets)
  if made_move:
    return True

  elif len(open_squares) > 0:
    # move
    x, y = curr.pos
    best_cell = best_move(grid[y][x], grid, open_squares)
    if best_cell:
      # print('best_cell', curr, curr.pos, 'to', best_cell.pos)
      move_to(curr, best_cell, grid)
      made_move = True
      attempt_attack(curr, targets)

  # print('no move!')
  return made_move

def move_to(sprite, cell, grid):
  x, y = sprite.pos
  grid[y][x].remove_occupant()
  sprite.pos = cell.pos
  cell.add_occupant(sprite)

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
    stats = ""
    for col in row:
      print(col, end="")
      if col.occupant is not None:
        stats += "%s(%d)," % (str(col.occupant), col.occupant.hp)
    print('    ', stats)

def clear_dead(sprites, grid):
  dead = [s for s in sprites if s.dead]
  sprites = [s for s in sprites if not s.dead]
  for d in dead:
    remove_from(d, grid)
  return sprites

def update(grid, sprites):
  for s in sort(sprites):
    try:
      turn(s, clear_dead(sprites, grid), grid)
    except NoTargetsException as e:
      return True, grid, clear_dead(sprites, grid)
  return False, grid, clear_dead(sprites, grid)

def run(grid, sprites):
  done = False
  counter = 0
  while not done:
    # time.sleep(1)
    if DEBUG:
      print('\nROUND', counter)
      print_grid(grid)
    done, grid, sprites = update(grid, sprites)
    counter += 1

  hps = sum([s.hp for s in sprites if not s.dead])
  print('remaining hp, rounds', hps, counter)
  return  hps * (counter-1)

def make_copy(grid, ap):
  new_grid = []
  new_sprites = []
  for row in grid:
    new_row = []
    for cell in row:
      if(cell.occupant):
        newsp = cell.occupant.copy()
        newcl = cell.copy()
        newcl.add_occupant(newsp)
        new_sprites.append(newsp)
        new_row.append(newcl)
        if newsp.type == SpriteType.ELF:
          newsp.ap = ap
          newsp.raise_exception = True
      else:
        new_row.append(cell.copy())
    new_grid.append(new_row)
  return new_grid, new_sprites

def min_win(gr, sp):
  ap = 3
  has_casualties = True
  while has_casualties:
    grid, sprites = make_copy(gr, ap)
    try:
      return run(grid, sprites)
    except ElfDeadException:
      has_casualties = True
      ap += 1
      continue
    break

  return ap

grid, sprites = parse(open('sample2.txt'))
assert(min_win(grid, sprites) == 4988)
assert(run(grid, sprites) == 27730)

grid, sprites = parse(open('sample4.txt'))
assert(run(grid, sprites) == 36334)

grid, sprites = parse(open('sample5.txt'))
assert(run(grid, sprites) == 18740)

grid, sprites = parse(open('sample6.txt'))
assert(min_win(grid, sprites) == 6474)
assert(run(grid, sprites) == 28944)

grid, sprites = parse(open('sample7.txt'))
assert(run(grid, sprites) == 27755)

grid, sprites = parse(open('sample8.txt'))
assert(run(grid, sprites) == 39514)

grid, sprites = parse(open('input.txt'))
assert(min_win(grid, sprites) == 37992)
assert(run(grid, sprites) == 206416)
