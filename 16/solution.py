from collections import namedtuple
from copy import copy
from ops import addr, addi, mulr, muli, \
              banr, bani, borr, bori, \
              setr, seti, gtir, gtri, \
              gtrr, eqir, eqri, eqrr

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
            ins = line.strip().split(' ')
            if(len(ins) > 1):
                program.append([int(i) for i in ins])
    return samples, program


OPCODES = [addr, addi, mulr, muli,
           banr, bani, borr, bori,
           setr, seti, gtir, gtri,
           gtrr, eqir, eqri, eqrr]


def test(samples):
    opcode_ids = [-1] * len(OPCODES)
    three_or_more = 0
    for sample in samples:
        matches = []
        o, a, b, c = sample.instruction

        for op in OPCODES:
            before = copy(sample.before)
            op(a, b, c, before)

            if before == sample.after:
                matches.append(op)
                if DEBUG:
                    print(op.__name__)

        if len(matches) >= 3:
            three_or_more += 1

        if len(matches) == 0:
            raise Exception('Unrecognized operation')
        elif len(matches) == 1:
            opcode_ids[o] = matches[0]
        elif len(matches) > 1:
            # eliminate founds
            unfound = [m for m in matches if m not in opcode_ids]
            if len(unfound) == 1:
                opcode_ids[o] = unfound[0]

    return three_or_more, opcode_ids


def run(opcodes, instructions):
    registers = [0, 0, 0, 0]
    for ins in instructions:
        o, a, b, c = ins
        opcodes[o](a, b, c, registers)
    return registers


def main():
    # samples, program = parse(open('input.txt'))
    samples, program = parse(open('sample.txt'))
    samples, program = parse(open('input.txt'))
    three_or_more, opcodes = test(samples)
    assert(three_or_more == 646)
    assert(run(opcodes, program)[0] == 681)
    print('tests pass')


main()
