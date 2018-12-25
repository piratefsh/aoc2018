# from: https://www.geeksforgeeks.org/sum-factors-number/

# Formula based Python3 code to find
# sum of all divisors of n.
import math as m

# Returns sum of all factors of n.
def sumofFactors(n):

    # Traversing through all
    # prime factors
    res = 1
    for i in range(2, int(m.sqrt(n) + 1)):
        count = 0
        curr_sum = 1
        curr_term = 1

        while n % i == 0:
            count = count + 1
            n = n / i;

            curr_term = curr_term * i;
            curr_sum += curr_term;

        res = res * curr_sum

    # This condition is to handle the
    # case when n is a prime number
    # greater than 2
    if n > 2:
        res = res * (1 + n)

    return res;

# driver code
sum = sumofFactors(10551296)
print ("Sum of all divisors is: ",sum)

# This code is contributed by Saloni Gupta