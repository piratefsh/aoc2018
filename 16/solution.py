from collections import namedtuple
from copy import copy
DEBUG = False
Sample = namedtuple('Sample', 'before instruction after')

def parse(file):
  samples = []
  program = []
  counter = 0
  is_samples = True
  line = True
  while line:
    line = file.readline()

    if line == '\n':
      counter += 1
      is_samples = False if counter >= 2 else is_samples
      continue

    if is_samples:
      before = eval(line.split(': ')[1])

      line = file.readline().strip()
      instruction = [int(i) for i in line.split(' ')]

      line = file.readline().strip()
      after = eval(line.split(': ')[1])

      samples.append(Sample(before, instruction, after))

      # consume newline
      line = file.readline()
    else:
      program.append(line.strip())
  return samples, program

def addr(A, B, C, R):
  R[C] = R[A] + R[B]
def addi(A, B, C, R):
  R[C] = R[A] + B
def mulr(A, B, C, R):
  R[C] = R[A] * R[B]
def muli(A, B, C, R):
  R[C] = R[A] * B
def banr(A, B, C, R):
  R[C] = R[A] & R[B]
def bani(A, B, C, R):
  R[C] = R[A] & B
def borr(A, B, C, R):
  R[C] = R[A] | R[B]
def bori(A, B, C, R):
  R[C] = R[A] | B
def setr(A, _, C, R):
  R[C] = R[A]
def seti(A, _, C, R):
  R[C] = A
def gtir(A, B, C, R):
  R[C] = 1 if A > R[B] else 0
def gtri(A, B, C, R):
  R[C] = 1 if R[A] > B else 0
def gtrr(A, B, C, R):
  R[C] = 1 if R[A] > R[B] else 0
def eqir(A, B, C, R):
  R[C] = 1 if A == R[B] else 0
def eqri(A, B, C, R):
  R[C] = 1 if R[A] == B else 0
def eqrr(A, B, C, R):
  R[C] = 1 if R[A] == R[B] else 0

OPCODES = [addr, addi, mulr, muli,
            banr, bani, borr, bori,
            setr, seti, gtir, gtri,
            gtrr, eqir, eqri, eqrr]

def test(samples):
  three_or_more = 0
  for sample in samples:
    matches = 0
    for op in OPCODES:
      o, a, b, c = sample.instruction
      before = copy(sample.before)
      op(a, b, c, before)

      if before == sample.after:
        matches += 1
        if DEBUG:
          print(op.__name__)
    if matches >= 3:
      three_or_more += 1

  return three_or_more

def main():
  # samples, program = parse(open('input.txt'))
  samples, program = parse(open('sample.txt'))
  samples, program = parse(open('input.txt'))
  print(samples)
  print(test(samples))

main()


