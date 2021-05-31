import argparse
import sys

from slanitsch.ue02_RSA.encryption import *

sys.path.insert(0, "../../..")

"""
Erweiterte Ausgabe, ja oder nein
"""
verbosity = False

"""
Argumente mit Typen und ob sie optional sind
"""
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
parser.add_argument("-o", "--outputfile", help="file to write output into", type=str)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-k", "--keygen", help="generate new keys with the given length", type=int)
group.add_argument("-e", "--encrypt", help="encrypt file", type=str)
group.add_argument("-d", "--decrypt", help="decrypt file", type=str)

args = parser.parse_args()

"""
Wenn das verbosity Argument im Aufruf vorhanden ist wird die erweiterte Ausgabe angemacht
"""
if args.verbosity:
    print("verbosity turned on")
    verbosity = True

"""
Schlüsselgeneration durch -k mit optionaler Angabe des Fields für den Key
Standardfile für Keys: keys.txt
"""
if args.keygen:
    if args.outputfile:
        print(args.outputfile)
        keygen(args.keygen, verbosity, args.outputfile, )
    else:
        keygen(args.keygen, verbosity)

"""
Verschlüsselung eines Files mit optionaler Angabe des Destinationfiles
Standardfile für den Output der Encryption: encrypted.txt
"""
if args.encrypt:
    if args.outputfile:
        encrypt(args.encrypt, args.outputfile, verbosity)
    else:
        encrypt(args.encrypt, "encrypted.txt", verbosity)

"""
Entschlüsselt ein File mit optionaler Angabe des Destinationfiles
Standardfile für den Output der Decryption: ergebnis.txt
"""
if args.decrypt:
    if args.outputfile:
        decrypt(args.decrypt, args.outputfile, verbosity)
    else:
        decrypt(args.decrypt, "ergebnis.txt", verbosity)