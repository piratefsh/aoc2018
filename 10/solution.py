import re
def parse(file):
  pattern = r'position=\<(.\d*), (.\d*)\> velocity=\<(.\d*), (.\d*)\>'
  return [[int(n) for n in re.match(pattern, line).groups()] for line in file]

def bounding_box(points):
  ox = sorted(points, key=lambda p: p[0])
  oy = sorted(points, key=lambda p: p[1])
  return (ox[0][0], oy[0][1]), (ox[-1][0], oy[-1][1])

def dist(a, b):
  ax, ay = a
  bx, by = b
  return (bx - ax) + (by - ay)

def run(points):
  tightest = (10000000000, 0)
  for i in range(100000):
    state = [(p[0] + p[2]*i, p[1]+ p[3]*i) for p in points]
    distance = dist(*bounding_box(state))
    td, ts = tightest
    if distance < td:
      tightest = (distance, i)

  print(tightest)

points = parse(open('input.txt'))
[print(str(point)) for point in points]
print(bounding_box(points))
print(run(points))