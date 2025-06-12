import cocotb
from cocotb.triggers import Timer
import numpy as np
from conversion_pkg import RealToHalf, DoubleFromHalf

DEBUG = 1
result_count = 0

async def toggle_clk(dut):
    global result_count
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if (dut.out_valid.value == 1):
        print("result = ", result_count, DoubleFromHalf(int(dut.c.value)))
        result_count += 1
        if result_count==10:
            result_count = 0
    if (DEBUG == 2):
        print("dut.out_valids[0]", dut.out_valids[0])
    if (DEBUG == 3):
        print("dut.count", int(dut.count.value))
    if (DEBUG == 0):
        print("dut.out_valid", dut.out_valid)


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
    dut.load_matrix.value = 0

async def test_vectors(dut, mults, b):
    c = int(len(b)/mults)
    for i in range(c):
        for j in range(mults):
            dut.vector_b[j].value = RealToHalf(b[c - mults - mults*i+j])
        dut.in_valid.value = 1
        await toggle_clk(dut)
    #dut.vector_b.value = [0, 0]

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))

def print_matrix_sums(mat):
    for i in range(10):
        print("row sum", i, sum(mat[i]))

@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    mat = np.zeros([10, 40], int)
    mat = mat.tolist()
    for i in range(10):
        for j in range(40):
            mat[i][j] = i+1

    print(mat)
    print_matrix_sums(mat)

    await load_matrix(dut, 10, 40, 2, mat)

    await check_vectors(dut)

    value = 1
    b = []
    for i in range(40):
        b.append(value)
    await test_vectors(dut, 2, b)

    dut.in_valid.value = 0
    for i in range(100):
        await toggle_clk(dut)

    for i in range(40):
        b[i] =                                                         b[i] * 2
    await test_vectors(dut, 2, b)

    for i in range(40):
        b[i] = b[i] * 2
    await test_vectors(dut, 2, b)

    dut.in_valid.value = 0;
    for i in range(20):
        await toggle_clk(dut);

