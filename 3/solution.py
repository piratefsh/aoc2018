# parse out x start, x end, y start, y end
def parse(line):
  nid, at, start, size = line.split(' ')

  # start: 1,3:
  px, py = map(int, start[0: -1].split(','))

  # size: 4x4
  sx, sy = map(int, size.split('x'))

  return nid, (px, py), (sx, sy)

def calc(p, s):
  px, py = p
  sx, sy = s
  return px, py, sx+px, sy+py


def part_a(file, scale=1000):
  fabric = [[0] * scale for i in range(0, scale)]
  overlaps = 0
  for line in file:
    nid, st, sz = parse(line)
    sx, sy, ex, ey = calc(st, sz)
    for x in range(sx, ex):
      for y in range(sy, ey):
        fabric[x][y] += 1
        overlaps = overlaps + 1 if fabric[x][y] == 2 else overlaps
  return overlaps, fabric

def part_b(file, fabric):
  for line in file:
    nid, st, sz = parse(line)
    sx, sy, ex, ey = calc(st, sz)
    occupied = 0
    for x in range(sx, ex):
      for y in range(sy, ey):
        occupied += fabric[x][y]
    if occupied == (ex-sx) * (ey-sy):
      return nid
  pass

assert(parse('#1 @ 1,3: 4x4') == ('#1', (1, 3), (4, 4)))
assert(parse('#200 @ 100,3: 400x400') == ('#200', (100, 3), (400, 400)))

overlaps, fabric = part_a(open('sample.txt'), 8)
assert(overlaps == 4)
assert(part_b(open('sample.txt'), fabric) == '#3')

overlaps, fabric = part_a(open('input.txt'))
assert(overlaps == 121259)
assert(part_b(open('input.txt'), fabric) == '#239')
print('all tests pass')