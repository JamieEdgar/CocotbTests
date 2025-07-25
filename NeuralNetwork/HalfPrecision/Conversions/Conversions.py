import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt
import numpy as np

def Bin2Half(bin_string):
    negative = 1
    if (bin_string[0] == "1"):
        negative = -1
    return negative

def DisplayValues(data):
    #print(Bin2Half(data), end='')
    print(data," ",end='')

displayed = False

@cocotb.test()
async def my_first_test(dut):
    global displayed
    """Try accessing the design."""

    for cycle in range(1000):
        dut.clk.value = 0
        #dut.a.value = 5
        #dut.b.value = 5
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
