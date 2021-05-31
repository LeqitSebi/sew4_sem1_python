# Jakob Bachl 4CN

"""
>>> is_prime_miller_rabin(1234567892)
False
>>> is_prime(1234567891)
True
"""

import random
import os

def is_prime_miller_rabin(n: int, k: int = 20) -> bool:
    """
    Method that checks if number n is really a prime
    :param n: number that will be checked if it is a prime
    :param k: how often it should be checked by the miller rabin principle
    :return: boolean, if it is a prime or not
    """
    if n <= 1:        raise ValueError('Number can not be checked to be a prime number')

#Test ob gerade Zahl
    elif n & 1 == 0:
        return False

    m = n - 1
    r = 0
    #in der While solange m gerade Zahl is
    while m & 1 == 0:
        m >>= 1
        r += 1
    m = n - 1
    d = m // (1 << r)
    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == m:
            continue
        for j in range(r - 1):
            x = pow(x, x, n)
            if x == m:
                break
        else:
            return False
    return True

def is_prime(number: int) -> bool:


    """
    Method that checks if number is a prime or not
    :param number: number that have to be checked
    :return: boolean, if it is a prime or not
    """

    if number <= 1:
        raise ValueError('Number can not be checked to be a prime number')
    if number in is_prime.cache:
        return True
    # test ob zahl gerade ist
    if number & 1 == 0:
        return False

    return is_prime_miller_rabin(number, 20)

# prime cache der einige Primzahlen beinhaltet
is_prime.cache = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def generate_prime(bits: int) -> int:
    """
    Method that generate a prime with a given number of bits
    :param bits: number of bits that the prime have to have
    :return: a number that is a prime
    """
    mask1 = 1 | (1 << (bits - 1))
#setzt letztes bit auf 1, dh ungerade zahl wird gmacht | das genau die bitzahl erreicht wird
    while True:
        n = random.getrandbits(bits) | mask1 # oder verknüpfen
        if is_prime(n):
            return n


if __name__ == '__main__':

    print(generate_prime(8))
    #print(is_prime(3))
    #print(is_prime(11))
    #print(is_prime(1234567891))
    #print(is_prime(1234567891*1234657981))