
from collections import namedtuple

Node = namedtuple('Node', 'value, children')

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
        p.children.append(node)

      curr_frame = parents
    elif c == '|':
      if peek(file) == ')':
        curr_frame.append(Node(None, []))
    elif c == '(':
      # stash curr frame and make new one
      stack.append(curr_frame)
      curr_frame = []
    elif c in 'NEWS':
      node = Node(c + consume_path(file), [])
      curr_frame.append(node)

    c = advance(file)
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
    for i in range(len(curr.children)):
      c = curr.children[len(curr.children) - i - 1]
      queue.append((c, depth + 1))

def traverse(node):
  stack = [node]
  while len(stack) > 0:
    curr = stack.pop(0)
    val, children = curr
    print(curr, end=' ')
    stack += children

paths = parse(open('sample1.txt'))
print_paths(paths)
traverse(paths)
paths = parse(open('sample2.txt'))
print(open('sample2.txt').readline())
print_paths(paths)
traverse(paths)

paths = parse(open('sample3.txt'))
print(open('sample3.txt').readline())
print_paths(paths)