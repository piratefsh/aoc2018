import sys, os
sys.path.insert(0, os.path.abspath('..'))
from shared import ops
# addr, addi, mulr, muli, \
# banr, bani, borr, bori, \
# setr, seti, gtir, gtri, \
# gtrr, eqir, eqri, eqrr
def parse(file):
  line = file.readline()
  ip_register = int(line.split(' ')[1][0])
  program = []
  line = file.readline()
  while line:
    statement = line.strip().split(' ')
    statement[1] = int(statement[1])
    statement[2] = int(statement[2])
    statement[3] = int(statement[3])
    program.append(statement)
    line = file.readline()

  return ip_register, program

def run(ipr, program, regsize=6):
  registers = [0] * regsize

  while registers[ipr] < len(program):
    # get curr line
    line_num = registers[ipr]
    line = program[line_num]
    op, a, b, c = line

    # increment pointer
    ops.addi(ipr, 1, ipr, registers)

    # fetch ip and run it
    fn = getattr(ops, op)
    fn(a, b, c, registers)

  return registers

ipr, program = parse(open('input.txt'))
print(program)
end = run(ipr, program)
print(end)