import cocotb
import random
import numpy as np
from cocotb.triggers import Timer
from matplotlib import pyplot as plt

debug = False
graph = False
random_input = False
bits = 8

async def toggle_clk(dut):
    dut.clk.value = 1
    await Timer(1, units="ns")
    dut.clk.value = 0
    await Timer(1, units="ns")

prevous = None
array_count = 0
array = np.zeros(1000)

async def print_debug(dut):
    global previous
    global array_count
    global array
    c = int(dut.s0_c.value)
    s3_dn = int(dut.s3_dn.value)
    s3_dn_d = int(dut.s3_dn_d.value)
    await toggle_clk(dut)
    result = int(dut.dn.value)
    if result > 8:
      result = result - 32
    array[array_count] = result
    array_count = array_count + 1
    if (array_count > 999):
        array_count = 0
    average = np.average(array)
    if (debug):
        print("dut.s0_c", c,
        "dut.s3_dn", s3_dn,
        "dut.s3_dn_d", s3_dn_d,
        "result", int(dut.dn.value),
        "average", average,
        array[array_count])
        if (previous != None):
            print("pre.s0_c", previous[0],
            "pre.s3_dn", previous[1],
            "pre.s3_dn_d", previous[2],
            "result", previous[3])
    previous = c, s3_dn, s3_dn_d, result

async def single_test(dut, f, repeats):
    global array_count, array_depth
    print("Before cycle loop")
    array_count = 0
    array_depth = repeats
    previous = None
    count = 0
    add_value = 126
    dut.f.value = f
    dut.clk.value = 0
    for cycle in range(repeats):
        if (random_input):
            dut.f.value = random.randint(1, 2**bits-1)
        await print_debug(dut)
        #await print_debug(dut)
        result = int(dut.dn.value)
        if (result > 8):
          result = result - 32
        count = count + 1
        if previous != None:
          if (graph):
              plt.plot([previous[0], count], [previous[1],result], '-')
          previous = count, result
        else:
          if (graph):
              plt.plot(count, result, '-')
          previous = count, result
        #if (count % 50 == 0):
        #  plt.pause(0.001)
    print("After cycle loop")
    average = np.average(array)
    maximum = np.max(array)
    minimum = np.min(array)
    fract = f/(2**bits-1)
    print("average", average, "input", fract, "ratio", average/fract)
    print("max", maximum)
    print("min", minimum)
    if maximum > 7:
        plt.plot(0,0,'o')
        plt.show()
    return fract, average

@cocotb.test()
async def my_first_test(dut):
    global random_input
    """Try accessing the design."""
    #for i in range(1000):
    #    #random_input = True # gives wider max and min
    #    await single_test(dut, random.randint(1,2**bits-1), 5000)
    fractions = []
    averages = []
    ratios = []
    for i in range(256):
        fract, average = await single_test(dut, i, 1000)
        fractions.append(fract)
        averages.append(average)
        ratios.append(average/fract)
    plt.plot(fractions, averages, "-")
    plt.show()
    plt.plot(ratios, "-")
    plt.show()

