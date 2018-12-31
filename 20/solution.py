
from collections import namedtuple

Node = namedtuple('Node', 'value, next')

def parse(file):
  c = file.read(1)
  root = None
  stack = []
  curr_frame = []
  while c:
    if c == '^':
      root = Node(c, [])
      stack.append([root])
    elif c == ')' or c =='$':
      # go back up one frame
      parents = stack.pop()
      p = parents[-1]

      for node in curr_frame:
        p.next.append(node)

      curr_frame = parents
    elif c == '|':
      if peek(file) == ')':
        curr_frame.append(Node('', []))
    elif c == '(':
      # stash curr frame and make new one
      stack.append(curr_frame)
      curr_frame = []
    elif c in 'NEWS':
      node = Node(c + consume_path(file), [])
      curr_frame.append(node)

    c = advance(file)

  print_paths(root)
  return root

def advance(file, n=1):
  return file.read(n)

def peek(file):
  pos = file.tell()
  peekv = file.read(1)
  file.seek(pos)
  return peekv

def consume_path(file):
  val = ''
  c = None
  while peek(file) in 'NEWS':
    c = advance(file)
    val += c
  return val

def print_paths(node):
  queue = [(node, 0)]
  while len(queue) > 0:
    curr, depth = queue.pop()
    print(' ' * depth + str(curr[0]))
    for i in range(len(curr.next)):
      c = curr.next[len(curr.next) - i - 1]
      queue.append((c, depth + 1))

def move(c, pos):
  x, y = pos

  if c == 'E':
    pos = (x + 1, y)
  elif c == 'W':
    pos = (x - 1, y)
  elif c == 'N':
    pos = (x, y - 1)
  elif c == 'S':
    pos = (x, y + 1)

  return pos

def traverse(node, graph={}, depths=[0], pos=(0,0)):
  path = node.value
  options = node.next

  new_depths = []
  for depth in depths:
    for p in path:
      pos = move(p, pos)
      depth += 1
      if pos in graph:
        graph[pos] = min(graph[pos], depth)
      else:
        graph[pos] = depth
    new_depths.append(depth)

  print(path, new_depths)

  if len(options) == 0:
    return new_depths, graph

  child_depths = []
  for option  in options:
    d, g = traverse(option, graph, new_depths, pos)
    child_depths += d

  # print('child', node.value, child_depths)
  return child_depths, graph

# paths = parse(open('sample1.txt'))
# print_paths(paths)
# traverse(paths)
paths = parse(open('sample2.txt'))
print(open('sample2.txt').readline())
# print_paths(paths)
dist, graph = traverse(paths)
for g in graph:
  print(g, ':', graph[g])

# paths = parse(open('sample3.txt'))
# print(open('sample3.txt').readline())
# dist, graph = traverse(paths)

# for g in graph:
#   print(g, ':', graph[g])
# print_paths(paths)
