import math

def power(x, y, serial):
#   Find the fuel cell's rack ID, which is its X coordinate plus 10.
# Begin with a power level of the rack ID times the Y coordinate.
# Increase the power level by the value of the grid serial number (your puzzle input).
# Set the power level to itself multiplied by the rack ID.
# Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
# Subtract 5 from the power level.
  # The rack ID is 3 + 10 = 13.
  rid = x + 10
  # The power level starts at 13 * 5 = 65.
  lvl = rid * y
  # Adding the serial number produces 65 + 8 = 73.
  lvl += serial
  # Multiplying by the rack ID produces 73 * 13 = 949.
  lvl = lvl * rid
  # The hundreds digit of 949 is 9.
  lvl = int(str(lvl)[-3])
  # Subtracting 5 produces 9 - 5 = 4.
  lvl -= 5
  return lvl

def make_grid(serial_number):
  return [[power(row, col, serial_number) for col in range(1, 301)]
     for row in range(1, 301)]

def total_power(grid, serial_number, window=3):
  biggest = 0
  pos = (0, 0)

  for row in range(300-window):
    for col in range(300-window):
      window_total = 0
      for i in range(row, row + window):
        for j in range(col, col + window):
          window_total += grid[i][j]

          if window_total > biggest:
            biggest = window_total
            pos = (row + 1, col + 1)

  return biggest, pos

def biggest_window(grid, serial_number):
  biggest = 0
  res = (0, 0, 0)
  store = [[0 for col in range(300)] for row in range(300)]
  for i in range(1, 301):
    size, pos = total_power(grid, serial_number, i)

    # store the size

    if size > biggest:
      res = (pos[0], pos[1], i)
  return res

assert(power(3, 5, 8) == 4)

assert(total_power(make_grid(18), 18) == (29, (33,45)))
assert(total_power(make_grid(42), 42) == (30, (21,61)))

assert(biggest_window(make_grid(18), 18) == (90,269,16))
# print(total_power(1308))