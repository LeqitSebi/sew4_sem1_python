from __future__ import annotations
from slanitsch.ue02_RSA.miller_rabin import generate_prime
import os
import math
import argparse
import sys


def generate_keys(bits):
    class Key:
        def __init__(self, key: int, modulus: int, key_bit_length: int):
            self._key = key
            self._modulus = modulus
            self._key_bit_length = key_bit_length

        @property
        def key(self) -> int:
            return self._key

        @property
        def modulus(self) -> int:
            return self._modulus

        @property
        def key_bit_length(self) -> int:
            return self._key_bit_length

        @property
        def key_byte_length(self) -> int:
            return math.ceil(self._key_bit_length / 8)

        def cipher(self, data: int or bytes, input_bytes: int = None, output_bytes: int = None,
                   remove_padding: bool = False) -> int or bytes:
            if type(data) == int:
                return pow(data, self.key, self.modulus)
            elif type(data) == bytes:
                cipher_text = b''
                for i in range(0, len(data), input_bytes):
                    num = int.from_bytes(data[i:i + input_bytes], byteorder='little', signed=False)
                    num = self.cipher(num)
                    cipher_text += int.to_bytes(num, output_bytes, byteorder='little', signed=False)
                if remove_padding:
                    pos = 0
                    while len(cipher_text) > -pos and cipher_text[pos - 1] == 0:
                        pos -= 1
                    cipher_text = cipher_text[0:pos]
                return cipher_text
            else:
                raise NotImplementedError

        def encrypt(self, data: bytes) -> bytes:
            return self.cipher(data, self.key_byte_length - 1, self.key_byte_length, remove_padding=False)

        def decrypt(self, data: bytes, last: bool = False) -> bytes:
            return self.cipher(data, self.key_byte_length, self.key_byte_length - 1, remove_padding=last)

        def save_to_file(self, file_name: str) -> None:
            file = open(file_name, 'w+')
            file.write('{}:{}:{}\n'.format(self.key_bit_length, self.key, self.modulus))
            file.close()

        @staticmethod
        def load_from_file(file_name: str) -> Key:
            file = open(file_name, 'r')
            array = [int(v) for v in file.readline().split(':')]
            return Key(array[1], array[2], array[0])

        def __str__(self) -> str:
            return '{{RSA-Key:{}:{}/{}}}'.format(self.key_bit_length, self.key, self.modulus)

        def __len__(self) -> int:
            return self.key_bit_length

    def egcd(a: int, b: int) -> (int, int, int):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = egcd(b % a, a)
            return g, x - (b // a) * y, y

    def modinv(a: int, m: int) -> int:
        g, x, y = egcd(a, m)
        if g != 1:
            raise AssertionError('modular inverse does not exist')
        else:
            return x % m

    def generate_keys(bits: int, insecure: bool = False) -> (Key, Key):
        """
        >>> pub, priv = generate_keys(1024)
        >>> for x in [2, 3, 7, 8, 10, 312, 783, 901, 1020, 2054, 46382]:
        ...     c = pow(x, pub.key, pub.modulus)
        ...     y = pow(c, priv.key, priv.modulus)
        ...     assert x == y
        """
        while True:
            p = generate_prime(math.ceil(bits / 2), urandom=(not insecure))
            q = generate_prime(math.floor(bits / 2), urandom=(not insecure))
            if p == q:
                continue
            n = p * q
            if n.bit_length() >= bits:
                break
        phi = (p - 1) * (q - 1)
        while True:
            try:
                e = int.from_bytes(os.urandom(phi.bit_length() // 8), byteorder='big', signed=False) | 1
                d = modinv(e, phi)
                break
            except AssertionError:
                pass
        return Key(e, n, bits), Key(d, n, bits)

    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('action', choices=['encrypt', 'decrypt', 'generate-keys'])
        parser.add_argument('-k', '--key-file', required=False,
                            help='The key file, the data should be encrypted/decrypted')
        parser.add_argument('--private-key', required=False,
                            help='The file, the private key should be saved in')
        parser.add_argument('--public-key', required=False,
                            help='The file, the public key should be saved in')
        parser.add_argument('-l', '--key-length', required=False, type=int,
                            help='The RSA bit length')
        parser.add_argument('-i', '--input-file', required=False)
        parser.add_argument('-o', '--output-file', required=False)
        args = parser.parse_args()

        if args.action == 'generate-keys':
            if args.key_length is None:
                parser.error('action generate-keys requires --key-length')
            private_file = args.private_key or 'priv.key'
            public_file = args.public_key or 'pub.key'
            pub, priv = generate_keys(args.key_length)
            pub.save_to_file(public_file)
            priv.save_to_file(private_file)
        elif args.action == 'encrypt':
            if args.input_file is None or args.output_file is None:
                parser.error('action encrypt requires --input-file and --output-file')
            key_file = args.key_file or 'priv.key'
            key = Key.load_from_file(key_file)
            input_file = open(args.input_file, 'rb')
            output_file = open(args.output_file, 'wb+')
            while True:
                data = input_file.read(key.key_byte_length - 1)
                if len(data) == 0:
                    break
                output_file.write(key.encrypt(data))
            output_file.close()
        elif args.action == 'decrypt':
            if args.input_file is None or args.output_file is None:
                parser.error('action decrypt requires --input-file and --output-file')
            key_file = args.key_file or 'pub.key'
            key = Key.load_from_file(key_file)
            input_file = open(args.input_file, 'rb')
            output_file = open(args.output_file, 'wb+')
            input_file.seek(0, 2)
            file_size = input_file.tell()
            input_file.seek(0, 0)
            while True:
                data = input_file.read(key.key_byte_length)
                if len(data) == 0:
                    break
                last = input_file.tell() == file_size or len(data) != key.key_byte_length
                output_file.write(key.decrypt(data, last=last))
            output_file.close()
        else:
            print('Invalid action!', file=sys.stderr)
            exit(1)
