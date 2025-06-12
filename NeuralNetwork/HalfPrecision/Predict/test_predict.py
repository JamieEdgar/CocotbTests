import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt
import numpy as np
import Precision as Prec

def Bin2Half(bin_string):
    negative = 1
    if (bin_string[0] == "1"):
        negative = -1
    return Prec.BinaryToHalf(bin_string)
    return negative

def DisplayValues(data):
    #print(Bin2Half(data), end='')
    print(data," ",end='')

displayed = False
current_image = 0
image_solutions = [7, 2, 1]

@cocotb.test()
async def my_first_test(dut):
    global displayed
    global current_image
    """Try accessing the design."""

    for cycle in range(5000):
        dut.clk.value = 0
        #dut.a.value = 5
        #dut.b.value = 5
        if (dut.done == 1):
            if displayed == False:
                displayed = True
                #s = np.shape(dut.W1)
                #print(s, s[0])
                #for i in range(s[0]):
                #    for j in range(s[1]):
                #    DisplayValues(dut.W1[i][0].value)
                print("Done has been received.")
                #print("X")
                #for i in range(28*28):
                #    if dut.x[i].value != 0:
                #        print("%d %f", i, dut.x[i].value)
                #for i in range(28*28):
                #    if dut.image_bytes[i].value != 0:
                #        print("image bytes %d %f", i, dut.image_bytes[i].value)
                print("Y")
                best = image_solutions[current_image]
                best_value = Bin2Half(str(dut.y[best].value))
                for i in range(10):
                    value = Bin2Half(str(dut.y[i].value))
                    print("%f %f", dut.y[i].value, value)
                    if (i != best):
                        assert value < best_value, "Wrong Image Selected"
                current_image = current_image + 1
        if (dut.done == 0):
            displayed = False
        #if (dut.noisy_ready == 1):
        #    print("out_valid = 1")
        #    PlotPoints(dut.noisy)
        #    print("After PlotPoints")
        await Timer(1, units="ns")
        dut.clk.value = 1
        #dut.a.value = 6
        #dut.b.value = 6
        await Timer(1, units="ns")

    #dut._log.info("my_signal_1 is %s a is %s b is %s c is %s", dut.my_signal_1.value , dut.a.value, dut.b.value, dut.c.value)
    #assert dut.my_signal_2.value[0] == 0, "my_signal_2[0] is not 0!"
