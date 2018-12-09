
def parse(file):
  return [int(n) for n in file.read().split(' ')]

def count(node):
  nchildren = node[0]
  nentries = node[1]

  # return if is leaf node
  if nchildren == 0:
    meta = sum(node[2: 2 + nentries]) if nentries > 0 else 0
    # print('leaf', meta, node[:2 + nentries])
    return meta, 2 + nentries

  currl = 0
  meta = 0

  for i in range(nchildren):
    m, l = count(node[2 + currl:])
    currl += l
    meta += m

  curr_end = 2 + currl + nentries

  meta += sum(node[curr_end - nentries : curr_end])

  # print('not', meta, node[:curr_end], curr_end)
  return (meta, curr_end)

data = parse(open('input.txt'))
print(len(data))
print(count(data))