# Jakob Bachl 4CN

def file2ints(path, length):
    """
    Method that translates a file to integer
    :param path: file path
    :param length: size/length
    :return:  ints from file
    """
    with open(path, 'rb') as f:
        byte = f.read(length)
        yield int.from_bytes(byte, 'little')
        while byte != b'':
            byte = f.read(length)
            yield int.from_bytes(byte, 'little')

if __name__ == '__main__':
    print(list(file2ints("test.txt", 2)))