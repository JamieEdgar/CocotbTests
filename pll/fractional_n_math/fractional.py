import numpy as np

print("fractional n pll examples")

def calc_values(n):
    # try a 16 17 divider
    a = 0
    b = 0
    found = False
    while found == False and a < n:
        a = a + 16
        if (n - a) % 17 == 0:
            found = True
            x = a/16
            y = (n-a)/17
            z = x + y
            print("for",n,"use",a/16,"and",(n-a)/17)
            print(x,y,z)
            print("division ratio",x*16+y*17)

    if found == False:
        print(n,"did not work")

def calc_values_test():
    calc_values(513)
    calc_values(103)

array = np.zeros(1000)
array_count = 0

def fractional_n(N, num, den):
    global array, array_count
    acc = 0
    for i in range(2000):
        acc = acc + num
        if acc > den:
            array[array_count] = N+1
            print(N+1, np.average(array))
            acc = acc -den
        else:
            print(N, np.average(array))
            array[array_count] = N
        array_count = array_count + 1
        if (array_count == 1000):
            array_count = 0

fractional_n(100, 13, 32)
print(13/32)






