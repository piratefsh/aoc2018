import re
import bisect

class Node:
  def __init__(self, name):
    self.name = name
    self.befores = []
    self.afters = []
    self.visited = False

  def add_before(self, node):
    self.befores.append(node)

  def add_after(self, node):
    self.afters.append(node)

  def ready(self):
    # has no befores, or no unvisited befores
    return len(self.befores) == 0 or len([b for b in self.befores if not b.visited]) == 0

  def visit(self):
    self.visited = True

  def __lt__(self, other):
    return self.name < other.name
  def __le__(self, other):
    return self.name <= other.name
  def __eq__(self, other):
    return self.name == other.name
  def __gt__(self, other):
    return self.name >= other.name
  def __ge__(self, other):
    return self.name >= other.name

  def __repr__(self):
    befs = ", ".join([b.name for b in self.befores])
    afts = ", ".join([a.name for a in self.afters])
    return "<%s befores: %s, afters: %s>" % (self.name, befs, afts)

def parse(file):
  nodes = {}
  for line in file:
    before, after = re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin', line).groups()

    if before not in nodes:
      nodes[before] = Node(before)
    if after not in nodes:
      nodes[after] = Node(after)

    nodes[before].add_after(nodes[after])
    nodes[after].add_before(nodes[before])

  # print(nodes.values())
  return nodes

def order(nodes):
  order_visited = []
  unvisited = sorted([n for n in nodes.values() if n.ready()])
  while len(unvisited) > 0:

    for n in unvisited:
      if n.ready():
        unvisited.remove(n)
        order_visited.append(n.name)
        n.visit()

        # add next steps
        for a in n.afters:
          if not a.visited and a not in unvisited:
            bisect.insort_left(unvisited, a)

        break

  return order_visited

nodes = parse(open('input.txt'))
print("".join(order(nodes)))


