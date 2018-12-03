def has_n(line, n):
  seen = dict()
  for c in line:
    seen[c] = seen[c] + 1 if c in seen else 1

  for c in seen:
    if seen[c] is n:
      return True
  return False

def num_diffs(left, right):
  diffs = 0
  diff_pos = []
  for i in range(len(left)):
    if left[i] is not right[i]:
      diffs = diffs + 1
      diff_pos.append(i)

  return diffs, diff_pos

def part_a(inputs):
  has2 = 0
  has3 = 0
  for line in inputs:
    if has_n(line, 2):
      has2 += 1
    if has_n(line, 3):
      has3 += 1
  return (has2 * has3)

def part_b(file):
  inputs = [line.strip() for line in file]
  half = int(len(inputs)/2)
  for left in inputs[0: half]:
    for right in inputs[half:]:
      n, diff_pos = num_diffs(left, right)
      if n == 1:
        return left[0: diff_pos[0]] + left[diff_pos[0] + 1:]
  return

assert(has_n('abcdef', 2) == False)
assert(has_n('bababc', 2) == True)
assert(has_n('bababc', 3) == True)
assert(has_n('abbcde', 2) == True)
assert(has_n('abbcde', 3) == False)
assert(has_n('aaa', 3) == True)
assert(has_n('aaaa', 3) == False)
assert(num_diffs('abcde', 'abcde') == (0, []))
assert(num_diffs('abcde', 'abxde') == (1, [2]))
assert(num_diffs('abcde', 'xyosa') == (5, [0, 1, 2, 3, 4]))

assert(part_b([
  'abcde',
  'fghij',
  'klmno',
  'pqrst',
  'fguij',
  'axcye',
  'wvxyz']) == 'fgij')
assert(part_b(open('input.txt')) == 'revtaubfniyhsgxdoajwkqilp')
print(part_a(open('input.txt')))
print(part_b(open('input.txt')))