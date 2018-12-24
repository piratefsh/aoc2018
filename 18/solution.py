OPEN = '.'
TREE = '|'
LUMBER = '#'

def parse(file):
  return [[c for c in line if not c == '\n'] for line in file]

def gprint(grid):
  for row in grid:
    for c in row:
      print(c, end="")
    print()
  print()

def update(c, pos, grid):
  x, y = pos
  neighbours = [grid[j][i] for i, j in [(x-1, y-1),
                (x, y-1),
                (x+1, y-1),
                (x-1, y),
                (x+1, y),
                (x+1, y+1),
                (x, y+1),
                (x-1, y+1)] if j in range(0, len(grid)) and i in range(0, len(grid[0]))]
  if c == OPEN:
    if neighbours.count(TREE) >= 3:
      return TREE
  if c == TREE:
    if neighbours.count(LUMBER) >= 3:
      return LUMBER
  if c == LUMBER:
    if neighbours.count(LUMBER) >= 1 and neighbours.count(TREE) >= 1:
      return LUMBER
    else:
      return OPEN
  return c

def count(grid):
    grid = [c for row in grid
              for c in row]
    return grid.count(TREE), grid.count(LUMBER)

def run(grid, n=10):
  end = n
  scores = []
  stable_for = 0
  while n > 0:
    grid = [[update(c, (x, y), grid) for x, c in enumerate(row)]
      for y, row in enumerate(grid)]
    n -= 1
    curr_score =  count(grid)
    scores.append(curr_score)
    # if curr_score == score:
    #   stable_for += 1
    #   if stable_for > 20:
    #     return grid
    print(end - n, curr_score, curr_score[0] * curr_score[1])
    # gprint(grid)
  return grid

grid = parse(open('sample.txt'))
grid = run(grid)
v1, v2 = count(grid)
assert v1*v2 == 1147

grid = parse(open('input.txt'))
grid = run(grid, 10)
v1, v2 = count(grid)
assert v1 * v2 == 605154

grid = parse(open('input.txt'))
grid = run(grid, 1000000000)
v1, v2 = count(grid)
print(v1 * v2)
