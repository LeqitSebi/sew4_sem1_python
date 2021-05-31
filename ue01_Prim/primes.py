#!/usr/bin/python3.7

import doctest
import math
import time

def primes():

    yield from primes.cache

    def is_prime(c):
        """
        Check if a number c is a prime number
        :param c: number to check
        :return: true (is a prime) or false (not a prime)

        >>> is_prime(1)
        true
        >>> is_prime(2)
        true
        >>> is_prime(7)
        true
        >>> is_prime(8)
        false
        >>> is_prime(12134512)
        false
        >>> is_prime(12134513)
        true
        """
        sqrt = math.sqrt(c)
        for p in primes.cache:
            if p > sqrt:
                break
            if c % p == 0:
                return False
        return True

    c = primes.cache[-1] + 2
    while True:
        while not is_prime(c):
            c += 2
        primes.cache.append(c)
        yield c
        c += 2


primes.cache = [2, 3, 5, 7, 11, 13]

if __name__ == '__main__':
    doctest.testmod()
    start = time.time_ns()
    pr = primes()
    for i in range(1, 400_001):
        p = next(pr)
        stop = time.time_ns()
        if i == 200_000:
            print("200000-te primzahl: {} ({:.3f} sec)".format(p, (stop - start) / 1_000_000_000))
        elif i == 400_000:
            print("400000-te primzahl: {} ({:.3f} sec)".format(p, (stop - start) / 1_000_000_000))