import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt
import numpy as np
import Precision as Prec

Prec.debug = False

def PlotPoints(points):
    print("PlotPoints")
    print(len(points), points[0], points[1])
    for i in range(int(len(points)/2)):
        x = int(points[2*i])
        y = int(points[2*i+1])
        if (x > 127):
            x = -1 - (255-x)
        if (y > 127):
            y = -1 - (255-y)
        plt.plot(x, y, "o")
        if i % 100 == 0:
            plt.pause(0.001)
        #plt.pause(0.005)
    plt.show()

def Bin2Half(bin_string):
    negative = 1
    if (bin_string[0] == "1"):
        negative = -1
    return negative

def DisplayValues(data):
    #print(Bin2Half(data), end='')
    print(data," ",end='')

displayed = False

async def reset(dut):
    dut.rstn.value = 1
    await clock_cycle(dut)
    dut.rstn.value = 0
    await clock_cycle(dut)
    dut.rstn.value = 1
    await clock_cycle(dut)


async def clock_cycle(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")

async def add_test(dut, a, b):
    dut.in_valid.value = 1;
    dut.a.value = Prec.BinToInt(Prec.SingleToBinary(a))
    dut.b.value = Prec.BinToInt(Prec.SingleToBinary(b))
    await clock_cycle(dut)
    if dut.out_valid.value == 1:
        print("out valid = 1")
        print("agtb", dut.a_gt_b.value)
        print("shifts", int(dut.ashift.value), int(dut.bshift.value))
        print("leading zeros", int(dut.leading_zeros.value))
        print(dut.a.value, dut.b.value, dut.c.value)
        print(Prec.BinaryToSingle(str(dut.a.value)),
              Prec.BinaryToSingle(str(dut.b.value)),
              Prec.BinaryToSingle(str(dut.c.value)))
        print(dut.sum.value)
    dut.in_valid.value = 0;
    await clock_cycle(dut)

@cocotb.test()
async def my_first_test(dut):
    global displayed
    """Try accessing the design."""

    dut.in_valid.value = 0;
    await clock_cycle(dut)

    await reset(dut)

    await add_test(dut, 0.1, 0.1)
    await add_test(dut, 0.1, -0.1)
    await add_test(dut, 127, 0.1)
    await add_test(dut, 0.1, 3e4)


    for cycle in range(10):
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
