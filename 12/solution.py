import math

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

def str_state(state):
  return "".join(['#' if c else '.' for c in state])

def total(state, offset):
  total = 0

  for i in range(0, len(state)):
    if state[i]:
      total += (i - offset)
  return total

def run(state, conditionals, generations=20):
  curr_gen = [False] + state + [False]
  tots = 0
  delta = 0
  seen_delta_count = 0
  offset = 1
  for g in range(generations):
    new_gen = [False] * len(curr_gen)
    for i in range(2, len(curr_gen) - 2):
      nb = curr_gen[i-2 : i + 3]
      for cond in conditionals:
        is_match, res = cond(nb)
        if(is_match):
          new_gen[i] = res
          break
    offset += 1
    curr_gen = [False] + new_gen + [False]
    new_tots = total(curr_gen, offset)
    new_delta = new_tots - tots

    if(delta == new_delta):
      seen_delta_count+=1
    else:
      seen_delta_count=0
      delta = new_delta

    # if seen new delta too many times, assume that it is always constant
    if seen_delta_count > 20:
      return (generations - g - 1) * delta + new_tots

    tots = new_tots
  return total(curr_gen, offset)

init, conditionals = parse(open('input.txt'))
assert(run(init, conditionals, generations=5 * 10**9) == 400000001480)