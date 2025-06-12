import cocotb
from cocotb.triggers import Timer
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

result_count = 0
clock_count = 0

async def toggle_clk(dut):
    global result_count
    global clock_count
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if (dut.out_valid.value == 1):
        print("result = ", result_count, DoubleFromHalf(int(dut.c.value)), "clock count", clock_count)
        result_count += 1
        if result_count > 49:
            result_count = 0
    if (DEBUG == 2):
        print("dut.out_valids[0]", dut.out_valids[0])
    if (DEBUG == 3):
        print("dut.count", int(dut.count.value))
    if (DEBUG == 0):
        print("dut.out_valid", dut.out_valid)
    clock_count += 1


async def setup(dut):
    dut.in_valid.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

async def load_matrix(dut, r, c, mults, mat):
    print("load matrix")
    for i in range(r):
        for j in range(int(c/mults)):
            for k in range(mults):
                # Note that rows are loaded in order, columns stream up.
                dut.matrix_a_in[k].value = RealToHalf(mat[i][c - mults -mults*j+k])
            dut.load_matrix.value = 1
            await(toggle_clk(dut))
            if DEBUG==2: print(dut.matrix_a_in.value)
    dut.load_matrix.value = 0

async def load_matrix_halves(dut, r, c, mults, mat):
    print("load matrix")
    for i in range(r):
        for j in range(int(c/mults)):
            for k in range(mults):
                # Note that rows are loaded in order, columns stream up.
                dut.matrix_a_in[k].value = (mat[i][c - mults -mults*j+k])
            dut.load_matrix.value = 1
            await(toggle_clk(dut))
            if DEBUG==2: print(dut.matrix_a_in.value)
    dut.load_matrix.value = 0

async def test_vectors(dut, mults, b):
    global clock_count
    clock_count = 0
    c = int(len(b)/mults)
    for i in range(c):
        for j in range(mults):
            dut.vector_b[j].value = RealToHalf(b[i * mults + j])  # vector goes in in order
        dut.in_valid.value = 1
        await toggle_clk(dut)
        if DEBUG==2: print(dut.vector_b.value)
    #dut.vector_b.value =
    dut.in_valid.value = 0
    for i in range(10):
        await toggle_clk(dut)

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))

def print_matrix_sums(mat):
    for i in range(20):
        print("row sum", i, sum(mat[i]))

async def general_tests(dut):
    ROWS = 50
    COLS = 784

    mat = np.zeros([ROWS, COLS], int)
    mat = mat.tolist()
    for i in range(ROWS):
        for j in range(COLS):
            mat[i][j] = i+1

    print(mat)
    print_matrix_sums(mat)

    await load_matrix(dut, ROWS, COLS, 4, mat)

    await check_vectors(dut)

    b = np.zeros([COLS], int)
    for i in range(COLS):
        b[i] = 1
    await test_vectors(dut, 4, b)

    dut.in_valid.value = 0
    for i in range(100):
        await toggle_clk(dut)

    for i in range(COLS):
        b[i] = b[i] * 2
    await test_vectors(dut, 4, b)

    for i in range(COLS):
        b[i] = b[i] * 2
    await test_vectors(dut, 4, b)

    dut.in_valid.value = 0;
    for i in range(100):
        await toggle_clk(dut)

def BytesToReal(data):
    result = []
    for i in range(len(data)):
        result.append(data[i]/255)
    return result

async def mnist_test(dut):
    print("mnist_test")
    W1 = LoadW1(network_filename)
    W1 = list(map(list, zip(*W1)))
    print(W1)
    print("size W1", len(W1))
    await load_matrix_halves(dut, 50, 784, 4, W1)
    image = LoadImage(image_filename, 0)
    image = BytesToReal(image)
    await test_vectors(dut, 4, image)
    dut.in_valid.value = 0;
    for i in range(100):
        await toggle_clk(dut)


@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    #await general_tests(dut)

    await mnist_test(dut)



