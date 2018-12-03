with open('input.txt') as file:
  result = 0
  track = dict()
  actions = []
  for line in file:
    parsed = int(line)
    actions.append(parsed)

  i = 0
  while not result in track:
    track[result] = True
    result = result + actions[i%len(actions)]
    i+=1

  print(result)

# main()