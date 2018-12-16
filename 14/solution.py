def solution(rounds):
  recipes = "37"
  elf1 = 0
  elf2 = 1
  for i in range(1, rounds + 9 - 2):
    score1 = int(recipes[elf1])
    score2 = int(recipes[elf2])
    newr = score1 + score2
    recipes = recipes + str(newr)
    elf1 = (1 + elf1 + score1) % len(recipes)
    elf2 = (1 + elf2 + score2) % len(recipes)

  return recipes[rounds:rounds + 10]

def solution2(target):
  recipes = "37"
  elf1 = 0
  elf2 = 1
  rounds = 1
  while(not recipes[-len(target):] == target):
    score1 = int(recipes[elf1])
    score2 = int(recipes[elf2])
    newr = score1 + score2
    recipes = recipes + str(newr)
    elf1 = (1 + elf1 + score1) % len(recipes)
    elf2 = (1 + elf2 + score2) % len(recipes)
    rounds += 1
  return recipes.find(target)

  return recipes[rounds:rounds + 10]
assert(solution(9) == '5158916779')
assert(solution2('01245') == 5)
assert(solution2('59414') == 2018)
assert(solution2('51589') == 9)
assert(solution2('92510') == 18)
assert(solution(5) == '0124515891')
assert(solution(18) == '9251071085')
print(solution2('793061'))
# print(solution(793061))
