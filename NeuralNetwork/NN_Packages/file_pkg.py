import struct

SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

# output real data[]
def ReadDoubles(fileName, offset, length):
    doubles = []
    with open(fileName, 'rb') as file:
        file.seek(offset, SEEK_SET)
        for i in range(length):
            # Read 8 bytes (size of a double)
            data = file.read(8)
            if not data:
                break  # End of file
            # Unpack the data as a double (using '<d' for little-endian)
            double_value = struct.unpack('<d', data)[0]
            doubles.append(double_value)
    return doubles

if __name__ == "__main__":
    print(ReadDoubles("../MNIST/mnist_network.bin", 4916, 10))

