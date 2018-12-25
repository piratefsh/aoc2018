3 mulr 2 3 4
4 eqrr 4 5 4
5 addr 4 1 1
6 addi 1 1 1
7 addr 2 0 0
8 addi 3 1 3
9 gtrr 3 5 4
10 addr 1 4 1
11 seti 2 4 1

Registers:
0 1 2 3 4 5


10 [232, 10, 79, 577, 0, 896] [<function addr at 0x10c225e18>, 1, 4, 1] [232, 10, 79, 577, 0, 896]
11 [232, 11, 79, 577, 0, 896] [<function seti at 0x10c2f0598>, 2, 4, 1] [232, 2, 79, 577, 0, 896]
3 [232, 3, 79, 577, 0, 896] [<function mulr at 0x10c2f01e0>, 2, 3, 4] [232, 3, 79, 577, 45583, 896]
4 [232, 4, 79, 577, 45583, 896] [<function eqrr at 0x10c2f08c8>, 4, 5, 4] [232, 4, 79, 577, 0, 896]
5 [232, 5, 79, 577, 0, 896] [<function addr at 0x10c225e18>, 4, 1, 1] [232, 5, 79, 577, 0, 896]
6 [232, 6, 79, 577, 0, 896] [<function addi at 0x10c2f0158>, 1, 1, 1] [232, 7, 79, 577, 0, 896]
8 [232, 8, 79, 577, 0, 896] [<function addi at 0x10c2f0158>, 3, 1, 3] [232, 8, 79, 578, 0, 896]
9 [232, 9, 79, 578, 0, 896] [<function gtrr at 0x10c2f0730>, 3, 5, 4] [232, 9, 79, 578, 0, 896]
10 [232, 10, 79, 578, 0, 896] [<function addr at 0x10c225e18>, 1, 4, 1] [232, 10, 79, 578, 0, 896]
11 [232, 11, 79, 578, 0, 896] [<function seti at 0x10c2f0598>, 2, 4, 1] [232, 2, 79, 578, 0, 896]

0 addi r1 + 16 -> r1
1 seti 1 -> r2
2 seti 1 -> r3
3 mulr r2 r3 -> r4 # save r2 * r3 to r4
4 eqrr r4 r5 -> r4 # is r4 == r5?
5 addr r4 r1 -> r1 # increment r1 by r4; if r4 is 0, go to 6, else 7
6 addi r1 1 -> r1  # increment r1 by 1; skip line 7
7 addr r2 + r0 -> r0 # increment r0 by r2
8 addi r3 1 -> r3  # increment r3 by 1 # increment multiplier r3
9 gtrr r3 r5 -> r4 # is r3 > r4? # r3 has passed 896?
10 addr r1 r4 -> r1 
11 seti 2 -> r1     # set r1 to 2 #loop back to 3
12 addi r2 + 1 -> r2# increment r2 by 1
13 gtrr r2 == r5 -> r4 # check if r2 is r5
14 addr r4 + r1 -> r1 # increment r1 by r4
15 seti 1 -> r1      # set r1 to 1