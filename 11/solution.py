import math

GRID_SIZE = 300

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
  return [[power(row, col, serial_number) for col in range(1, GRID_SIZE+1)]
     for row in range(1, GRID_SIZE+1)]

def total_power(grid, serial_number, window=3):
  biggest = 0
  pos = (0, 0)

  for row in range(GRID_SIZE-window):
    for col in range(GRID_SIZE-window):
      window_total = 0
      for i in range(row, row + window):
        for j in range(col, col + window):
          window_total += grid[i][j]

          if window_total > biggest:
            biggest = window_total
            pos = (row + 1, col + 1)

  return biggest, pos

def all_window(x, y, grid, serial_number):
  window_total = 0
  biggest = 0
  pos = ()

  # print('xy', x, y)

  for n in range(1, GRID_SIZE - max(x, y)):
    # print(x + n, end=", ")
    # breakpoint()
    # print('size', n)
    for i in range(n - 1):
      x1, y1 = (x + i, y + n - 1)
      window_total += grid[x1][y1]
      # print(x1, y1)

    for i in range(n - 1):
      x2, y2 = (x + n - 1, y + i)
      window_total += grid[x2][y2]
      # print(x2, y2)

    tx, ty = x + n-1, y + n-1
    # print(tx, ty)
    window_total += grid[tx][ty]

    if window_total > biggest:
      biggest = window_total
      pos = (x+1, y+1, n)

  return biggest, pos

def biggest_window(grid, serial_number):
  biggest = 0
  res = (0, 0, 0)

  for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
      size, pos = all_window(row, col, grid, serial_number)
      if size > biggest:
        biggest = size
        res = pos
  return biggest, res

assert(power(3, 5, 8) == 4)

# assert(total_power(make_grid(18), 18) == (29, (33,45)))
# assert(total_power(make_grid(42), 42) == (30, (21,61)))

# print(biggest_window(make_grid(18), 18))
# assert(biggest_window(make_grid(18), 18) == (90,269,16))
print(biggest_window(make_grid(1308), 1308))