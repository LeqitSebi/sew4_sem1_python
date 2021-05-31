import os
import random


def is_prime_miller_rabin(n, k):
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def is_prime(number: int) -> bool:
    if number <= 1:
        raise ValueError('Number can not be checked to be a prime number')
    elif number & 1 == 0 or number in is_prime.cache:
        return False
    for p in is_prime.cache:
        if number % p == 0:
            return False
        elif p > number:
            break
    return is_prime_miller_rabin(number, 20)


is_prime.cache = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def generate_prime(bits: int, urandom: bool = False) -> int:
    if bits < 8:
        raise ValueError('Number of bits should be not smaller than 8 to provide realistic prime numbers')
    mask1 = 1 | 1 << (bits - 1)
    mask2 = ~(1 << (bits))
    while True:
        if urandom:
            n = int.from_bytes(os.urandom(bits // 8 + 1), byteorder='big', signed=False) & mask2 | mask1
        else:
            n = random.getrandbits(bits) | mask1
        if is_prime(n):
            return n


if __name__ == '__main__':
    print(generate_prime(1024, urandom=True))
