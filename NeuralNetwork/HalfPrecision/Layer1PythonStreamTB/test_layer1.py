import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt
import numpy as np

import sys
from pathlib import Path
proj_path = Path(__file__)
pkgs = proj_path.parent.parent.parent / 'NN_Packages/'
sys.path.append(str(pkgs))

from testbench_functions_pkg import LoadW1, Loadb1, LoadW2, Loadb2, LoadImage
from conversion_pkg import RealToHalf, DoubleFromHalf, DoubleToHalf

network_filename = "../../MNIST/mnist_network.bin"
image_filename = "../../MNIST/t100-images.idx3-ubyte"

DEBUG = 1
MULTS = 2

result_count = 0
clock_count = 0

check_x_dot_W1 = 0
x_dot_W1_count = 0

async def toggle_clk(dut):
    global result_count
    global clock_count
    global x_dot_W1_count
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if check_x_dot_W1 == 1:
        if dut.done_x_dot_W1.value == 1:
            print("x_dot_W1", x_dot_W1_count, DoubleFromHalf(int(dut.x_dot_W1.value)))
            x_dot_W1_count += 1
    if dut.out_valid.value == 1:
        print("result", result_count, DoubleFromHalf(int(dut.layer1_out.value)), "clock_count", clock_count)
        result_count += 1
        if result_count == 50:
            result_count = 0
    clock_count += 1
    
async def setup(dut):
    dut.in_valid.value = 0
    dut.load_W1;value = 0
    dut.load_b1.value = 0
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)      

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

async def load_matrix_halves(dut, r, c, mults, mat):
    print("load_matrix_halves")
    for i in range(r):
        for j in range(int(c/mults)):
            for k in range(mults):
                # Note that rows are loaded in order, columns stream up.
                dut.neuron_data_in[k].value = (mat[i][c - mults -mults*j+k])
            dut.load_W1.value = 1
            await(toggle_clk(dut))
            #print(dut.neuron_data_in.value)
    dut.load_W1.value = 0

async def load_vector_halves(dut, l, mults, vec):
    print("load vector halves")
    for i in range(int(l/mults)):
        for j in range(mults):
            dut.neuron_data_in[j].value = (vec[l-mults-(i*mults)+j])
        dut.load_b1.value = 1
        await(toggle_clk(dut))
        #print(dut.neuron_data_in.value)
    dut.load_b1.value = 0

async def test_vector(dut, l, mults, vec):
    print("load vector")
    for i in range(int(l/mults)):
        for j in range(mults):
            dut.x[j].value = RealToHalf(vec[(i*mults)+j])
        dut.in_valid.value = 1
        await(toggle_clk(dut))
    dut.in_valid.value = 0

async def load_arrays(dut):
	print("mnist_test")
	W1 = LoadW1(network_filename)
	W1 = list(map(list, zip(*W1)))	# these are already half values
	#print("W1", W1)
	await load_matrix_halves(dut, 50, 784, MULTS, W1)
	b1 = Loadb1(network_filename)
	print("b1",b1)
	await load_vector_halves(dut, 50, 1, b1)

def BytesToReal(data):
    result = []
    for i in range(len(data)):
        result.append(data[i]/255)
    return result

async def send_image(dut, image_number):
    image = LoadImage(image_filename, image_number)
    image = BytesToReal(image)
    #print("image", image)
    print("max image", np.max(image))
    await test_vector(dut, 784, MULTS, image)
    dut.in_valid.value = 0;



@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    await load_arrays(dut)

    await send_image(dut, 0)
    await send_image(dut, 0)

    for i in range(500):
        await toggle_clk(dut)




