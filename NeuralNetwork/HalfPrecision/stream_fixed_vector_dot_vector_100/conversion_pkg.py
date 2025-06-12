import struct
import ctypes

DEBUG = 0

# input [15:0] half;
def SingleFromHalf(half):
    sign = int(half / 2**15)
    exponent = 127 + int(half/2**10) % 2**5 - 15
    mantissa = int(half % 2**10)*2**13
    if (half % 2**15 == 0):
        return 0
    else:
        return int(sign * 2**31 + exponent * 2**23 + mantissa)

# input real  a_real;
def RealToHalf(a_real):
  float_bits = ctypes.c_float(a_real)
  a_single = ctypes.c_uint.from_buffer(float_bits)
  a_single = a_single.value
  sign = int(a_single/2**31)
  if (int(a_single/2**23 % 2**8) < (127 - 15)):
      return 0
  else:
      if (int(a_single/2**23 % 2**8) > (127 + 16)):
          return sign * 2**15 + 2**15 - 1;
      else:
          a_exp = int(a_single/2**23 % 2**8) - 127 + 15;
          if (a_single==0):
              return 0
          else:
              return sign * 2**15 + a_exp * 2**10 + int(a_single / 2**13) % 2**10;

  return int_bits.value


# input [15:0] half;
def DoubleFromHalf(half):
    sign = int(half / 2**15)
    exponent = 1023 + int(half/2**10) % 2**5 - 15
    mantissa = int(half % 2**10)*2**42
    if (half % 2**15 == 0):
        return 0.0
    else:
        double_bits = int(sign * 2**63 + exponent * 2**52 + mantissa)
        return struct.unpack('d', struct.pack('Q', double_bits))[0]

#       1         11            52
# sign 63  exp 62-52 mantissa 51-0
# 01111111 = 127  01111111111 = 1023

# input real  a_real;
def DoubleToHalf(a_real):
  return RealToHalf(a_real)

if __name__ == "__main__":
    print(SingleFromHalf(1000))
    print(RealToHalf(3.5))
    print(DoubleFromHalf(1000))
    print(DoubleToHalf(3.5))
