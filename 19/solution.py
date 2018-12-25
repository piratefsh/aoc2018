import sys, os
sys.path.insert(0, os.path.abspath('..'))
from shared import ops

DEBUG = True

def parse(file):
  line = file.readline()
  ip_register = int(line.split(' ')[1][0])
  program = []
  line = file.readline()
  while line:
    statement = line.strip().split(' ')
    statement[0] = getattr(ops, statement[0])
    statement[1] = int(statement[1])
    statement[2] = int(statement[2])
    statement[3] = int(statement[3])
    program.append(statement)
    line = file.readline()

  return ip_register, program

def run(ipr, program, regzero=0, regsize=6):
  registers = [0] * regsize
  ip = registers[ipr]
  registers[0] = regzero

  counter = 0

  while ip < len(program):
    counter += 1
    if counter > 30:
      exit()
    # set register with latest ip
    ops.seti(ip, None, ipr, registers)

    # custom loop optimization
    if ip == 3:
      print('CUSTOM')
      ops.custom(registers)
      # jump to exit of loop
      return registers
    # get curr line
    line = program[ip]
    op, a, b, c = line

    if DEBUG:
      print(ip, registers, line, end=" ")

    # run statement
    op(a, b, c, registers)

    # get ip from register
    ip = registers[ipr]
    ip = ip + 1
    if DEBUG:
      print(registers)

  return registers

ipr, program = parse(open('input.txt'))
# end = run(ipr, program)
# assert(end == [2040, 256, 897, 897, 1, 896])
end = run(ipr, program, 1)
print(end)