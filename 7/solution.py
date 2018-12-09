import re
import bisect

class Node:
  def __init__(self, name, base_duration):
    self.name = name
    self.befores = []
    self.afters = []
    self.visited = False
    self.duration = ord(name) - 64 + base_duration
    self.occupied = False

  def add_before(self, node):
    self.befores.append(node)

  def add_after(self, node):
    self.afters.append(node)

  def ready(self):
    # is not already occupied and has no befores, or no unvisited befores
    return not self.occupied and (len(self.befores) == 0 or len([b for b in self.befores if not b.visited]) == 0)

  def occupy(self):
    self.occupied = True

  def visit(self):
    self.visited = True

  def __repr__(self):
    befs = ", ".join([b.name for b in self.befores])
    afts = ", ".join([a.name for a in self.afters])
    return "<%s befores: %s, afters: %s>" % (self.name, befs, afts)

class Worker:
  def __init__(self, wid, queue, done_queue):
    self.busy = False
    self.id = wid
    self.duration = 0
    self.curr_node = None
    self.queue = queue
    self.done_queue = done_queue

  def occupy(self, node):
    node.occupy()
    self.busy = True
    self.curr_node = node
    self.duration = node.duration

  def finish_node(self, n):
    n.visit()
    self.done_queue.append(n.name)

  def tick(self):
    self.duration -= 1

    # if done with work, free self
    if self.duration == 0:
      self.busy = False
      self.finish_node(self.curr_node)

  def __repr__(self):
    return "Worker %d" % self.id

def order(nodes, workers=1):
  done_queue = []
  total_nodes = len(nodes.values())

  # sort nodes
  queue = sorted([n for n in nodes.values()], key=lambda n: n.name)

  # create workers
  workers = [Worker(i, queue, done_queue) for i in range(workers)]
  ticks = 0

  while len(done_queue) != total_nodes:
    for n in queue:
      # if node is ready for use
      if n.ready():
        # if has available workers,
        avail_workers = [w for w in workers if not w.busy]
        if len(avail_workers) > 0:
          # put someone to work
          avail_workers[0].occupy(n)

    # advance time
    [w.tick() for w in workers]
    ticks += 1

  return "".join(done_queue), ticks

def parse(file, base_duration=0):
  nodes = {}
  for line in file:
    before, after = re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin', line).groups()

    if before not in nodes:
      nodes[before] = Node(before, base_duration=base_duration)
    if after not in nodes:
      nodes[after] = Node(after, base_duration=base_duration)

    nodes[before].add_after(nodes[after])
    nodes[after].add_before(nodes[before])

  # print(nodes.values())
  return nodes

nodes = parse(open('sample.txt'), 0)
assert(order(nodes, workers=2) == ('CABFDE', 15))

nodes = parse(open('input.txt'), 60)
assert(order(nodes, workers=5) == ('FHRXMQSNEGWZIBCLOUATDJPKVY', 917))

print('tests pass')
