class DoubleNode:
  def __init__(self, value):
    self.next = None
    self.prev = None
    self.value = value
    self.visited = False

  def set_next(self, node):
    self.next = node
    node.prev = self

  def visit(self):
    self.visited = True

  def __repr__(self):
    # return str(self.value)
    return "<Node %d, next %d, prev %d>" % (self.value, self.next.value, self.prev.value)

def print_loop(node):
  curr = node.next
  while curr != node:
    print(curr.value, end=' ')
    curr = curr.next
  print()

def play(nplayers=1, nmarbles=10):
  players = [0] * nplayers
  curr = DoubleNode(0)
  start = curr

  curr.set_next(curr)

  for i in range(1, nmarbles):
    player = i % nplayers
    if i % 23 == 0:
      # special case
      # go back 7
      for _ in range(7):
        curr = curr.prev

      # add score
      players[player] += curr.value + i

      # replace
      curr.prev.set_next(curr.next)
      curr = curr.next
    else:
      # normal case
      # insert two next clockwise
      new_node = DoubleNode(i)

      clasp = curr.next.next
      new_node.set_next(clasp)
      curr.next.set_next(new_node)
      curr = new_node

  # print_loop(start)
  return max(players)

assert(play(9, 25) == 32)
assert(play(452, 71250) == 388844)