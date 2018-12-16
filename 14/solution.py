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
assert(solution(9) == '5158916779')
assert(solution(5) == '0124515891')
assert(solution(18) == '9251071085')
print(solution(793061))
