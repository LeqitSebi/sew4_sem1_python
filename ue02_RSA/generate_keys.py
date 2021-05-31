# Jakob Bachl 4CN

"""
>>> keys = generate_keys(1024)
>>> list = [secrets.randbits(1024) for x in range(1,50)]
>>> ergebnis = True
>>> for x in list:
...     c = pow(x,keys[0],keys[2])
...     y = pow(c,keys[1],keys[2])
...     ergebnis = ergebnis and x == y
>>> ergebnis
True
"""

from bachl.sew4_sem1_python.ue04_rsa.millerRabin import generate_prime
import secrets

def extended_gcd(a, b):
    """
    Errechnet das Inverse Element und den GGT
    :param a: Teil 1 des ggt
    :param b: Teil 2 des ggt
    :return: der größte gemeinsame Teiler und das modverse Element
    """
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
        quotient = old_r // r
        (old_r, r) = (r, old_r - quotient * r)
        (old_s, s) = (s, old_s - quotient * s)
        (old_t, t) = (t, old_t - quotient * t,)
    return [old_r, old_s, old_t]


def generate_keys(number_of_bits, verbosity=False):
    """
    generiert ein Keypaar mit bitanzahl
    :param number_of_bits: die Bitanzahl des Keypaars
    :param verbosity: verbosity
    :return: the keypair
    """
    # p is hälfte vo number bits
    p = generate_prime(number_of_bits >> 1)
    #falls die bitlänge zu kurz is +1
    q = generate_prime(number_of_bits - p.bit_length() + 1)
    #nochmal checken das die Bitlänge passt
#    while q.bit_length() <= number_of_bits - p.bit_length():
#       q = generate_prime(number_of_bits - p.bit_length() + 1)
    if verbosity: print("Calculating n")
    n = p * q
    phi = (p - 1) * (q - 1)
    if verbosity:
        print("Generating Key 1")
    e = secrets.randbits(number_of_bits)
    #solange in der while bis teilerfremd dh !=1
    while extended_gcd(phi, e)[0] != 1:
        e = secrets.randbits(number_of_bits)
    if verbosity: print("Generating Key 2")
    # d ist inverse element
    d = extended_gcd(e, phi)[1]
    # % damit fix positiv is
    # zwei Files machen, damit privater Key nicht geshared wird
    # nur öffentlichgen
    return [e, d % phi, n]


if __name__ == '__main__':
    print(generate_keys(9))