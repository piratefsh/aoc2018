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

def custom(R):
  while R[2] < R[5]:
    R[3] = 1
    while R[3] < R[5]:
      R[4] = R[2] * R[3]
      if R[4] == R[5]:
        R[0] = R[0] + R[2]
      R[3] += 1
    R[2] += 1
