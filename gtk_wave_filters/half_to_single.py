#!/usr/bin/env python3
import sys
import struct

# input [15:0] half;
def DoubleFromHalf(half):
    half = int(half)
    sign = int(half / 2**15)
    exponent = 1023 + int(half/2**10) % 2**5 - 15
    mantissa = int(half % 2**10)*2**42
    if (half % 2**15 == 0):
        return 0.0
    else:
        double_bits = int(sign * 2**63 + exponent * 2**52 + mantissa)
        return struct.unpack('d', struct.pack('Q', double_bits))[0]

def SingleFromHalf(half):
    half = int(half, 16)
    sign = int(half / 2**15)
    exponent = 127 + int(half/2**10) % 2**5 - 15
    mantissa = int(half % 2**10)*2**13
    if (half % 2**15 == 0):
        return 0
    else:
        single_bits = int(sign * 2**31 + exponent * 2**23 + mantissa)
        return struct.unpack('f', struct.pack('I', single_bits))[0]

def main():
    fh_in = sys.stdin
    fh_out = sys.stdout

    while True:
        # incoming values have newline
        l = fh_in.readline()
        if not l:
            return 0
        test = SingleFromHalf(l)
        # outgoing filtered values must have a newline
        fh_out.write(str(test)+"\n")
        fh_out.flush()

if __name__ == '__main__':
	sys.exit(main())
