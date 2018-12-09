import re
import bisect

class Node:
  def __init__(self, name, base_duration=0):
    self.name = name
    self.befores = []
    self.afters = []
    self.visited = False
    self.duration = ord(name) - 65 + 1 + base_duration

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

class Worker:
  def __init__(self, wid, queue, done_queue):
    self.busy = False
    self.id = wid
    self.duration = 0
    self.curr_node = None
    self.queue = queue
    self.done_queue = done_queue

  def occupy(self, node):
    print(str(self) + ' occupied with ' + node.name)
    self.busy = True
    self.curr_node = node
    self.duration = node.duration

  def finish_node(self, n):
    print(n.name + ' finished')
    n.visit()
    self.done_queue.append(n.name)
    # for a in n.afters:
    #   if not a.visited and a not in self.queue:
    #     bisect.insort_left(self.queue, a)

  def tick(self):
    self.duration -= 1
    if self.duration == 0:
      self.busy = False
      self.finish_node(self.curr_node)
      print(str(self) + ' freed')

  def __repr__(self):
    return "Worker %d" % self.id

def order(nodes, workers=1):
  done_queue = []
  total_nodes = len(nodes.values())
  queue = sorted([n for n in nodes.values()])
  workers = [Worker(i, queue, done_queue) for i in range(workers)]
  has_busy_workers = False

  ticks = 0

  while len(done_queue) != total_nodes:
    for n in queue:
      if n.ready():
        # if has available workers,
        avail_workers = [w for w in workers if not w.busy]
        has_busy_workers = len(avail_workers) > 0
        if len(avail_workers) > 0:
          # put someone to work

          queue.remove(n)
          avail_workers[0].occupy(n)

    # advance time
    [w.tick() for w in workers]
    ticks += 1
    print('tick', ticks)

  return "".join(done_queue), ticks

nodes = parse(open('sample.txt'))
print(order(nodes, workers=2))
# assert(order(nodes, workers=1) == 'CABDFE')


