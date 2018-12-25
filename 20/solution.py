
from collections import namedtuple

Node = namedtuple('Node', 'value, children')

def parse(file):
  c = file.read(1)
  root = None
  stack = []
  curr_frame = []
  while c:
    print(stack)
    print(curr_frame)
    print()
    if c == '^':
      root = Node(c, [])
      stack.append(root)
    elif c == '$' or c == ')':
      parents = stack.pop()
      for p in parents:
        for node in curr_frame:
          p.children.append(node)
      curr_frame = parents

      if c == '$':
        break
    elif c == '(':
      # save curr frame
      stack.append(curr_frame)

      # new frame
      curr_frame = []
    elif c in 'NEWS':
      node = Node(c + consume_snippet(file), [])
      curr_frame.append(node)

    c = file.read(1)
  return root

def peek(file):
  pos = file.tell()
  peekv = file.read(1)
  file.seek(pos)
  return peekv

def consume_snippet(file):
  val = ''
  c = None
  while peek(file) in 'NEWS':
    c = file.read(1)
    val += c
  return val

def print_paths(node):
  queue = [(node, 0)]
  while len(queue) > 0:
    curr, depth = queue.pop(0)
    print(' ' * depth + curr[0])
    for c in curr.children:
      queue.append((c, depth + 1))

paths = parse(open('sample1.txt'))
print_paths(paths)

print(open('sample2.txt').readline())
paths = parse(open('sample2.txt'))
print_paths(paths)

print(open('sample3.txt').readline())
paths = parse(open('sample3.txt'))
print_paths(paths)