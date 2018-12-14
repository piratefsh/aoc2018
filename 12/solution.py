def parse(file):
  initial_state = file.readline().split(':')[1].strip()
  file.readline()

  conditionals = []

  for line in file:
    args, res = line.split(' => ')
    matches = " and ".join(["p[%d] == %s" % (i, str(a == '#'))  for i, a in enumerate(args)])
    fn_str = 'lambda p : (%s, %s)' % (matches, str(res[0] == '#'))
    fn = eval(fn_str)
    conditionals.append(fn)

  return [s == '#' for s in initial_state], conditionals

def neighbours(i, state):
  if(i == 0):
    return [False, False] + state[i: i+3]
  if(i == 1):
    return [False] + state[i-1: i+3]
  if i == len(state) - 1:
    return state[i - 2: i + 1] + [False, False]
  if i == len(state) - 2:
    return state[i - 2: i + 2] + [False]

  return state[i-2 : i + 3]

def str_state(state):
  return "".join(['#' if c else '.' for c in state])

def run(state, conditionals, generations=20):
  curr_gen =  state
  offset = 0
  ori_length = len(curr_gen)
  for g in range(generations):
    print(str_state(curr_gen))
    new_gen = [False] * len(curr_gen)
    for i in range(0, len(curr_gen)):
      nb = neighbours(i, curr_gen)
      for cond in conditionals:
        is_match, res = cond(nb)
        if(is_match):
          new_gen[i] = res
          break
    offset += 1
    curr_gen = [False] + new_gen + [False]

  total = 0
  print('offset', offset)
  print(ori_length, len(curr_gen))
  for i in range(0, len(curr_gen)):
    if curr_gen[i]:
      total += (i - offset)
  return total, str_state(curr_gen)

init, conditionals = parse(open('input.txt'))
init, conditionals = parse(open('sample.txt'))
# print(state, conditionals)
assert(neighbours(0, [True, True, True, False, False]) == [False, False, True, True, True])
assert(neighbours(1, [True, False, True, False, False]) == [False, True, False, True, False])
assert(neighbours(4, [False, False, True, True, True]) == [True, True, True, False, False])
assert(neighbours(3, [False, True, True, True, False]) == [True, True, True, False, False])
# print(str_state(init))
print(run(init, conditionals, generations=20))