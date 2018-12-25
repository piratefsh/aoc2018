
from collections import namedtuple

Node = namedtuple('Node', 'value, children')

def parse(file):
  c = file.read(1)
  root = None
  curr = None
  while c:
    if c == '^':
      n = file.read(1)
      root = Node(n, [])
      curr = root
    elif c == '$':
      break
    elif c in 'NEWS':
      node = Node(c, [])
      _, children = curr
      children.append(node)
      curr = node
    c = file.read(1)
  return root

def print_paths(node):
  queue = [(node, 0)]
  while len(queue) > 0:
    curr, depth = queue.pop(0)
    print(' ' * depth + curr[0])
    for c in curr.children:
      queue.append((c, depth + 1))
paths = parse(open('sample1.txt'))
print_paths(paths)