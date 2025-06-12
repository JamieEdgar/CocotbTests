import math

debug = False

def IntToBin(value):
    if debug: print("IntToBin")
    if debug: print("value =", value)
    temp = value
    result = ""
    while value > 0:
        if (value % 2) != 0:
            result = "1" + result
        else:
            result = "0" + result
        value = value // 2
    if debug: print("result =", result)
    return result

def BinToInt(value):
    if debug: print("BinToInt")
    if debug: print("value =", value)
    result = 0
    slen = len(value)
    for i in range(len(value)):
        if value[i] == "1":
            result = result + pow(2,slen - i - 1)
    if debug: print("result =", result)
    return result

def GetBinExponent(exponent_digits):
    exponent = BinToInt(exponent_digits) - 15
    return exponent

def GetBinNumber(number_digits):
    number = BinToInt(number_digits) / pow(2, 10)
    return number

def BinaryToHalf(value):
    sign = 1
    if len(value) != 16:
        print("Not a valid half float")
        return
    else:
        if value[1:6] == "00000":
            return 0
        if value[0] == "1":
            sign = -1
            if debug: print("negative number")
    exponent_digits = value[1:6]
    number_digits = "1" + value[6:16]
    if debug: print(sign, exponent_digits, number_digits)
    exponent = GetBinExponent(exponent_digits)
    if debug: print("exponent_digits",exponent_digits, exponent)
    number = GetBinNumber(number_digits)
    if debug: print("number_digits",number_digits, number)
    result = sign * number * pow(2, exponent)
    if debug: print("result =",sign * number * pow(2, exponent))
    return result

def GetHalfExponent(value):
    if debug: print("log2 = ", math.log2(value))
    result = int(math.log2(value))
    if debug: print(result)
    resultStr = IntToBin(result+15)
    while len(resultStr) < 5:
        resultStr = "0" + resultStr
    return result, resultStr

def GetHalfDigits(value, exponent):
    #print(value, exponent)
    value = value / pow(2, exponent)
    #print(value)
    value = value - 1
    result = ""
    for i in range(10):
        #print(i, value)
        value = value * 2
        if value > 1:
            result = result + "1"
            value = value - 1
        else:
            result = result + "0"
    return result

def HalfToBinary(value):
    if debug: print("")
    if debug: print("Input =", value)
    if value < 0:
        sign = "1"
        value = -value
    else:
        sign = "0"
    exponent, exponentStr = GetHalfExponent(value)
    if debug: print("Exponent =", exponentStr)
    digits = GetHalfDigits(value, exponent)
    result = sign + exponentStr + digits
    if debug: print("Binary =", result)
    return result



