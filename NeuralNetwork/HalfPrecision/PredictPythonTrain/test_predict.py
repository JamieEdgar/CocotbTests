import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt
import numpy as np

import sys
from pathlib import Path
proj_path = Path(__file__)
pkgs = proj_path.parent.parent.parent / 'NN_Packages/'
sys.path.append(str(pkgs))

import Precision as Prec
from testbench_functions_pkg import LoadW1, Loadb1, LoadW2, Loadb2, LoadImage
from conversion_pkg import RealToHalf, DoubleFromHalf, DoubleToHalf, MatrixHalfToReal, VectorHalfToReal, BytesToReal

network_filename = "../../MNIST/mnist_network.bin"
image_filename = "../../../fashion/t10k-images-idx3-ubyte"

LAYER1_MULTS = 4
DEBUG = False
display_layer1_output = 0
result_count = 0
clock_count = 0
last_result_count = 0
confidence = []

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

def check_for_result(dut):
    global result_count
    global current_image
    global confidence
    global clock_count
    global last_result_count
    if display_layer1_output == 1:
        if dut.out_valid_layer1.value == 1:
            print("layer1 out data", dut.layer1_out.value, DoubleFromHalf(dut.layer1_out.value))
    if dut.out_valid.value == 1:
        clocks_between_results = clock_count - last_result_count
        last_result_count = clock_count
        result = VectorHalfToReal(dut.y.value)
        print("Result", result_count, result, "clocks_between_results", clocks_between_results)
        result_count += 1
        for i in range(10):
            value = Bin2Half(str(dut.y[i].value))
            print("y",i, value)
        best = image_solutions[current_image]
        best_value = Bin2Half(str(dut.y[best].value))
        for i in range(10):
            value = Bin2Half(str(dut.y[i].value))
            print("%f %f", dut.y[i].value, value)
            #if (i != best):
            #    assert value < best_value, "Wrong Image Selected for image " + str(current_image)
        confidence.append(best_value)
        print("NN selected the best image for ", current_image)
        current_image += 1
    clock_count += 1

"""
async def toggle_clk(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    check_for_result(dut)
"""

async def load_matrix_halves(dut, r, c, mults, mat, label):
    print("load_matrix_halves")
    for i in range(r):
        for j in range(int(c/mults)):
            for k in range(mults):
                # Note that rows are loaded in order, columns stream up.
                dut.neuron_data_in[k].value = (mat[i][c - mults -mults*j+k])
            #print(label, "neuron_data_in", i, VectorHalfToReal(dut.neuron_data_in.value))
            await toggle_clk(dut)
            #print(dut.neuron_data_in.value)

async def load_vector_halves(dut, l, mults, vec, label):
    print("load vector halves")
    for i in range(int(l/mults)):
        for j in range(mults):
            dut.neuron_data_in[j].value = (vec[l-mults-(i*mults)+j])
        print(label, "neuron_data_in", i, VectorHalfToReal(dut.neuron_data_in.value))
        await(toggle_clk(dut))
        #print(dut.neuron_data_in.value)

async def load_parameters(dut):
    global LAYER1_MULTS
    print("load parameters")

    print("loading w1data")
    w1data = LoadW1(network_filename)
    w1data = list(map(list, zip(*w1data)))
    if (DEBUG): print("w1data", w1data)
    dut.load_W1.value = 1
    await load_matrix_halves(dut, 50, 784, LAYER1_MULTS, w1data, "W1")
    dut.load_W1.value = 0

    print("loading b1data")
    b1data = Loadb1(network_filename)
    if (DEBUG): print("b1data", b1data)
    dut.load_b1.value = 1
    await load_vector_halves(dut, 50, 1, b1data, "b1")
    dut.load_b1.value = 0


    print("loading w2data")
    w2data = LoadW2(network_filename)
    w2data = list(map(list, zip(*w2data)))
    if (DEBUG): print("w2data", w2data)
    dut.load_W2.value = 1
    await load_matrix_halves(dut, 10, 50, 1, w2data, "W2") # other input is ignored
    dut.load_W2.value = 0

    b2data = Loadb2(network_filename)
    print("loading b2data")
    if (DEBUG): print("b2data", b2data)
    dut.load_b2.value = 1
    await load_vector_halves(dut, 10, 1, b2data, "b2") # other input is ignored
    dut.load_b2.value = 0

async def release_reset(dut):
    dut.in_valid.value = 0
    dut.load_W1;value = 0
    dut.load_b1.value = 0
    dut.load_W2.value = 0
    dut.load_b2.value = 0
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    dut.in_valid.vlue = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

def CreateHalves(image_bytes):
    halves = []
    divisor = 255.0;
    for i in range(784):
        next_half = int(image_bytes[i]) / divisor;
        halves.append(DoubleToHalf(next_half))
    return halves

async def test_vector(dut, l, mults, vec):
    print("load vector")
    for i in range(int(l/mults)):
        for j in range(mults):
            dut.x[j].value = RealToHalf(vec[(i*mults)+j])
        dut.in_valid.value = 1
        await(toggle_clk(dut))
    dut.in_valid.value = 0

async def test_image(dut, image_number):
    global LAYER1_MULTS
    print("test image")
    image = LoadImage(image_filename, image_number)
    image = BytesToReal(image)
    if (DEBUG): print("image_data", image_number, image)
    print("max image", np.max(image))

    print("loading image data")
    await test_vector(dut, 784, LAYER1_MULTS, image)

    count = 0
    while (count < 0):            # 0 works with latest setup
        await toggle_clk(dut)
        count = count + 1
        if count % 100 == 0:
            print(count)


async def hold_reset_low(dut, count):
    dut.rstn.value = 0
    for i in range(count):
        await toggle_clk(dut)
    dut.rstn.value = 1

@cocotb.test()
async def my_first_test(dut):
    global LAYER1_MULTS
    LAYER1_MULTS = int(dut.LAYER1_MULTS.value)
    print("LAYER1_MULTS", dut.LAYER1_MULTS.value)

    await release_reset(dut)
    await load_parameters(dut)

    for i in range(10):
        print("test image", i)
        await test_image(dut, i)

    for i in range(1000):
        await toggle_clk(dut)

    print("Confidence for selected images", confidence)
