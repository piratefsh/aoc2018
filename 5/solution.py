def polymerize(line):
  curr = 0
  while curr < len(line) - 1:
    curr = 0 if curr < 0 else curr
    if opposite(line[curr], line[curr+1]):
      line = line[0 : curr] + line[curr + 2 : ]
      curr -= 1
    else:
      curr += 1

  return line

def find_shortest_with_exclusion(line, exclude):
  curr = 0
  while curr < len(line) - 1:
    curr = 0 if curr < 0 else curr

    if line[curr].upper() == exclude:
      line = line[0 : curr] + line[curr + 1 : ]
      curr -= 1

    elif opposite(line[curr], line[curr + 1]):
      line = line[0 : curr] + line[curr + 2 : ]
      curr -= 1
    else:
      curr += 1

  return line

def find_shortest(line):
  shortest = (None, 100000)
  for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    res = find_shortest_with_exclusion(line, c)
    if len(res) < shortest[1]:
      print(c, len(res))
      shortest = (c, len(res))

  return shortest

def opposite(a, b):
  return abs(ord(a) - ord(b)) == 32

assert(opposite('z', 'Z') == True)
assert(opposite('N', 'n') == True)
assert(opposite('n', 'n') == False)
soln = polymerize("dabAcCaCBAcCcaDAA")
assert(len(soln) == 11)
soln = polymerize(open('input.txt').read())
assert(len(soln) == 10564)
soln = find_shortest(open('input.txt').read())
assert(soln == ('P', 6336))
print((soln))