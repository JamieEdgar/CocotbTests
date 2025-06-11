import cocotb
import numpy as np
import random
from cocotb.triggers import Timer
from matplotlib import pyplot as plt

async def toggle_clk(dut):
    dut.clk.value = 1
    await Timer(1, units="ns")
    dut.clk.value = 0
    await Timer(1, units="ns")

BITS = None
previous = None
debug = False
graph = False
random_order = False
array_count = 0
array_depth = 10000
array = np.zeros(array_depth)

async def print_debug(dut):
    global previous
    global array_count
    global array
    c = int(dut.s0_c.value)
    s2_dn = int(dut.s2_dn.value)
    s2_dn_d = int(dut.s2_dn_d.value)
    await toggle_clk(dut)
    result = int(dut.dn.value)
    if result > 4:
      result = result - 16
    array[array_count] = result
    array_count = array_count + 1
    if (array_count > array_depth-1):
        array_count = 0
    average = np.average(array)
    if (debug):
        print("dut.s0_c", c,
        "dut.s2_dn", s2_dn,
        "dut.s2_dn_d", s2_dn_d,
        "result", result,
        "average", average,
        array[array_count])
        if (previous != None):
            print("pre.s0_c", previous[0],
            "pre.s2_dn", previous[1],
            "pre.s2_dn_d", previous[2],
            "result", previous[3])
    previous = c, s2_dn, s2_dn_d, result

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
        if (random_order):
            dut.f.value = random.randint(1,255)
        await print_debug(dut)
        #await print_debug(dut)
        result = int(dut.dn.value)
        if (result > 4):
          result = result - 16
        count = count + 1
        if previous != None:
          if (graph):
              plt.plot([previous[0], count], [previous[1],result], '-')
          previous = count, result
        else:
          if (graph):
              plt.plot(count, result, '-')
          previous = count, result
        if (count % 50 == 0):
          if (graph):
            plt.pause(0.001)
    print("After cycle loop")
    average = np.average(array[0:array_depth])
    maximum = np.max(array[0:array_depth])
    minimum = np.min(array[0:array_depth])
    fract = f / (2**BITS-1)
    print("average", average, "f/(2**BITS-1)", fract, "ratio", average/fract)
    print("Max", maximum)
    print("Min", minimum)

    if (maximum > 3):
        plt.plot(0, 0, '-')
        plt.show()
    if (graph):
        print("graph", graph)
        plt.show()
    return fract, average

async def random_input(dut, repeats):
    print("Before cycle loop")
    previous = None
    count = 0
    add_value = 126
    dut.clk.value = 0
    for cycle in range(repeats):
        dut.f.value = random.randint(1,255)
        await print_debug(dut)
        #await print_debug(dut)
        result = int(dut.dn.value)
        if (result > 4):
          result = result - 16
        count = count + 1
        if previous != None:
          if (graph):
              plt.plot([previous[0], count], [previous[1],result], '-')
          previous = count, result
        else:
          if (graph):
              plt.plot(count, result, '-')
          previous = count, result
        if (count % 50 == 0):
          if (graph):
            plt.pause(0.001)
    print("After cycle loop")
    average = np.average(array)
    maximum = np.max(array)
    minimum = np.min(array)
    print("average", average)
    print[("Max", maximum)]
    print("Min", minimum)

    if (maximum > 3):
        plt.plot(0,0,'o')
        plt.show()

async def linear_input(dut, start, stop,  repeat):
    print("Before cycle loop")
    previous = None
    count = 0
    add_value = 126
    dut.f.value = start
    dut.clk.value = 0
    for i in range(start, stop):
        for j in range(repeat):
            dut.f.value = i
            await print_debug(dut)
            #await print_debug(dut)
            result = int(dut.dn.value)
            if (result > 4):
              result = result - 16
            count = count + 1
            if previous != None:
                if (graph):
                    plt.plot([previous[0], count], [previous[1],result], '-')
            else:
                if (graph):
                    plt.plot(count, result, '-')
            previous = count, result
            if (count % 50 == 0):
                if (graph):
                    plt.pause(0.001)
    print("After cycle loop")
    average = np.average(array)
    maximum = np.max(array)
    minimum = np.min(array)
    print("average", average)
    print("Max", maximum)
    print("Min", minimum)

    #if (maximum > 3):
    #    plt.plot(0, 0, '-')
    plt.show()

@cocotb.test()
async def my_first_test(dut):
    global random_order
    global BITS, graph
    BITS = dut.BITS.value
    #random_order = True
    """Try accessing the design."""
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
    graph=True
    await single_test(dut, 0, 1000)
    await single_test(dut, 1, 5000)
    #await linear_input(dut, 1, 255,  100)
    #await random_input(dut, 5000) # This test shows max goes to 4 and min to -3
