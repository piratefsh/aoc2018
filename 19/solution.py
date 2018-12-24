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
  counter = 0
  ip = registers[ipr]

  while ip < len(program):
    counter +=1 
    if counter > 10:
      return registers

    # set register with ip
    ops.seti(ip, None, ipr, registers)

    # get curr line
    line = program[ip]
    op, a, b, c = line

    print(ip, registers, line, end=" ")


    # fetch ip and run it
    fn = getattr(ops, op)
    fn(a, b, c, registers)

    # reset ip from register
    ip = registers[ipr]
    ip = ip + 1
    print(registers)

  return registers

ipr, program = parse(open('sample.txt'))
print(program)
end = run(ipr, program)
assert(end[1] == 5)