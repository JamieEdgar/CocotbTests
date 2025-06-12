import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt
import numpy as np
import Precision as Prec
import sys
from pathlib import Path
proj_path = Path(__file__)
pkgs = proj_path.parent.parent.parent / 'NN_Packages/'
sys.path.append(str(pkgs))

from conversion_pkg import DoubleToHalf, MatrixHalfToReal, VectorHalfToReal
from testbench_functions_pkg import LoadW1, Loadb1, LoadW2, Loadb2, LoadImage

DEBUG = False

network_filename = "../../MNIST/mnist_network.bin"
image_filename =  "../../MNIST/t100-images.idx3-ubyte"

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
image_solutions = [7, 2, 1, 0, 4, 1, 4, 9, 6, 9]
single_done_layer1 = 0

def check_for_result(dut):
    global current_image
    global single_done_layer1
    if dut.half_predict1.done_layer1 == 1:
        if single_done_layer1 == 0:
            print("layer one result", VectorHalfToReal(dut.half_predict1.l.value))
            single_done_layer1 = 0
    if dut.done.value == 1:
        print("image complete")
        for i in range(10):
            value = Bin2Half(str(dut.y[i].value))
            print("y",i, value)
        best = image_solutions[current_image]
        best_value = Bin2Half(str(dut.y[best].value))
        for i in range(10):
            value = Bin2Half(str(dut.y[i].value))
            print("%f %f", dut.y[i].value, value)
            if (i != best):
                assert value < best_value, "Wrong Image Selected"
        print("NN selected the best image for ", current_image)
        current_image += 1

async def toggle_clock(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    check_for_result(dut)

async def load_parameters(dut):
    print("load parameters")

    print("loading w1data")
    w1data = LoadW1(network_filename)
    if (DEBUG): print("w1data", w1data)
    dut.load_W1.value = 1
    for i in range(784):
        if (DEBUG): print("i = ", i)
        for j in range(50):
            dut.neuron_data_in.value = w1data[783-i][49-j]
            await toggle_clock(dut)
    dut.load_W1.value = 0

    print("loading b1data")
    b1data = Loadb1(network_filename)
    if (DEBUG): print("b1data", b1data)
    dut.load_b1.value = 1
    for i in range(50):
        dut.neuron_data_in.value = b1data[49-i]
        await toggle_clock(dut)
    dut.load_b1.value = 0

    print("loading w2data")
    w2data = LoadW2(network_filename)
    if (DEBUG): print("w2data", w2data)
    dut.load_W2.value = 1
    for i in range(50):
        if (DEBUG): print("i = ", i)
        for j in range(10):
            dut.neuron_data_in.value = w2data[49-i][9-j]
            await toggle_clock(dut)
    dut.load_W2.value = 0

    b2data = Loadb2(network_filename)
    print("loading b2data")
    if (DEBUG): print("b2data", b2data)
    dut.load_b2.value = 1
    for i in range(10):
        dut.neuron_data_in.value = b2data[9-i]
        await toggle_clock(dut)
    dut.load_b2.value = 0

async def release_reset(dut):
    dut.rstn.value = 1
    await toggle_clock(dut)
    dut.rstn.value = 0
    dut.start.vlue = 0
    await toggle_clock(dut)
    dut.rstn.value = 1
    await toggle_clock(dut)

def CreateHalves(image_bytes):
    halves = []
    divisor = 255.0;
    for i in range(784):
        next_half = (int(image_bytes[i]) / divisor)
        halves.append(DoubleToHalf(next_half))
    return halves

async def test_image(dut, image):
    print("test image")
    image_data = LoadImage(image_filename, image)
    if (DEBUG): print("image_data", image, image_data)
    halves = CreateHalves(image_data)
    if (DEBUG): print("halves", halves)

    print("loading image data")
    dut.load_x.value = 1
    for i in range(784):
        dut.neuron_data_in.value = halves[783-i]
        await toggle_clock(dut)
    dut.load_x.value = 0

    dut.x.value = halves
    dut.start.value = 1
    await toggle_clock(dut)
    dut.start.value = 0
    count = 0
    while (count < 3):            # 0 fails 4 works
        await toggle_clock(dut)   # image 0 gives 0.4985
        count = count + 1
        if count % 100 == 0:
            print(count)


async def hold_reset_low(dut, count):
    dut.rstn.value = 0
    for i in range(count):
        await toggle_clock(dut)
    dut.rstn.value = 1

@cocotb.test()
async def my_first_test(dut):
    global displayed
    global current_image
    """Try accessing the design."""

    await release_reset(dut)
    await load_parameters(dut)

    for i in range(10):
        print("test image", i)
        await test_image(dut, i)

    for i in range(1000):
        await toggle_clock(dut)

