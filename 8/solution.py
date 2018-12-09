
def parse(file):
  return [int(n) for n in file.read().split(' ')]

def count(node, val_fn):
  nchildren = node[0]
  nentries = node[1]

  # return if is leaf node
  if nchildren == 0:
    meta = sum(node[2: 2 + nentries]) if nentries > 0 else 0
    # print('leaf', meta, node[:2 + nentries])
    return meta, 2 + nentries

  currl = 0

  children_vals = []

  for i in range(nchildren):
    m, l = count(node[2 + currl:], val_fn)
    currl += l
    children_vals.append(m)

  curr_end = 2 + currl + nentries
  meta_vals = node[curr_end - nentries : curr_end]

  meta = val_fn(meta_vals, children_vals)

  # print('meta vals', meta_vals)
  # print('children vals', children)
  # print('not', meta, node[:curr_end], curr_end)
  return (meta, curr_end)

def val_a(meta_vals, children_vals):
  return sum(meta_vals) + sum(children_vals)

def val_b(meta_vals, children_vals):
  norm_meta = [m-1 for m in meta_vals]
  return sum([children_vals[m] for m in norm_meta
    if m >= 0 and m < len(children_vals)])

assert(count(parse(open('input.txt')), val_b) == (25752, 16079))
assert(count(parse(open('input.txt')), val_a) == (41454, 16079))
print('tests pass')