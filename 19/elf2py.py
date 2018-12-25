r1 = 1
r2 = r3 = r4 = r5 = 0

r1 = 16
r5 = (2 * 2) * 19 * 11
r4 = 2 * 22 + 16
r5 = r5 + r4

r4 = 27
r4 = (r4 * 28 + 29) * 30 * 14 * 32
r5 = r5 + r4
r0 = 0

r2 = 1

print(r2, r3, r5)

while r2 < r5:
  r3 = 1
  while r3 < r5:
    print(r2, r3)
    x = r2 * r3
    if x == r5:
      r0 = r0 + r2
    r3 += 1

  r2 += 1

# find the sum of all divisors of r5=10551296
