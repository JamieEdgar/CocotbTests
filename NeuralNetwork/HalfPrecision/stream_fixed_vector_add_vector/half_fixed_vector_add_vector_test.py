import cocotb
from cocotb.triggers import Timer
import numpy as np
from conversion_pkg import RealToHalf, DoubleFromHalf

DEBUG = 1

async def toggle_clk(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if (dut.out_valid.value == 1):
        print("result = ", DoubleFromHalf(int(dut.c.value)))
    if (DEBUG == 2):
        print("dut.out_valids[0]", dut.out_valids[0])
    if (DEBUG == 0):
        print("dut.in_valid", dut.in_valid, end=" ")
        print("dut.count", int(dut.count.value), end=" ")
        print("dut.out_valid", dut.out_valid, end= " ")
        print("result = ", DoubleFromHalf(int(dut.c.value)))
    if (DEBUG == 2):
        print("dut.half_vector_dot_vector1.in_valid", dut.half_vector_dot_vector1.in_valid, end=" ")
        print("dut.half_vector_dot_vector1.out_valid_mult[0]", dut.half_vector_dot_vector1.out_valid_mult[0])
        print("dut.half_vector_dot_vector1.c_mult[0]", DoubleFromHalf(int(dut.half_vector_dot_vector1.c_mult[0].value)))
        print("dut.half_vector_dot_vector1.c_mult[1]", DoubleFromHalf(int(dut.half_vector_dot_vector1.c_mult[1].value)))




async def setup(dut):
    dut.in_valid.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

async def load_vector(dut, l, vec):
    print("load matrix")
    for i in range(int(l)):
        dut.vector_a_in.value = RealToHalf(vec[l - 1 - i])
        dut.load_a.value = 1
        await(toggle_clk(dut))

async def test_vectors(dut, b):
    l = int(len(b))
    for i in range(l):
        dut.vector_b.value = RealToHalf(b[l - 1 - i])
        dut.in_valid.value = 1
        await toggle_clk(dut)

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))

def print_matrix_sums(mat):
    for i in range(10):
        print("row sum", i, sum(mat[i]))

@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    vec = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    await load_vector(dut, 10, vec)

    #await check_vectors(dut)

    b = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    await test_vectors(dut, b)

    await test_vectors(dut, b)

    dut.in_valid.value = 0
    for i in range(100):
        await toggle_clk(dut)

    for i in range(10):
        b[i] = b[i] * 2
    await test_vectors(dut, b)

    for i in range(10):
        b[i] = b[i] * 2
    await test_vectors(dut, b)

    dut.in_valid.value = 0;
    for i in range(10):
        await toggle_clk(dut);

