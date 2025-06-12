import cocotb
from cocotb.triggers import Timer
import numpy as np
from conversion_pkg import RealToHalf, DoubleFromHalf

DEBUG = 1

async def toggle_clk(dut):
    global vec_sum
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if (dut.out_valid.value == 1):
        result = DoubleFromHalf(int(dut.c.value))
        print("result = ", result, result - vec_sum)
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

async def load_vector(dut, l, mults, vec):
    print("load fixed vector")
    for i in range(int(l/mults)):
        for j in range(int(mults)):
            #print(r - 1 - i, c - 1 -mults*j+k)
            dut.vector_a_in[j].value = RealToHalf(vec[l - mults - mults*i+j])
        dut.load_a.value = 1
        await(toggle_clk(dut))
        if (DEBUG == 2): print_vector(dut.vector_a_in.value)
    dut.load_a.value = 0
    for i in range(int(l/mults)):
        await(toggle_clk(dut))

async def test_vectors(dut, mults, b):
    c = int(len(b)/mults)
    for i in range(c):
        for j in range(mults):
            dut.vector_b[j].value = RealToHalf(b[c*2 - mults - mults*i+j])
        dut.in_valid.value = 1
        await toggle_clk(dut)
    dut.in_valid.value = 0
    for i in range(c):
        await toggle_clk(dut)       # have to wait to input next data for now.
    #dut.vector_b.value = [0, 0]

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))

vec_sum = 0

def print_vector_sum(vec):
    global vec_sum
    vec_sum = sum(vec)
    print("vec sum", sum(vec))

def print_vector(vec):
    print("Length = ", len(vec))
    if DEBUG==2: print("vec", vec)
    vec2 = []
    for i in range(len(vec)):
        value = int(vec[i])
        vec2.append(DoubleFromHalf(value))
        if DEBUG == 2: print(i, value, DoubleFromHalf(value))
    print("vec2", vec2)

async def single_test(dut, LENGTH):
    #await check_vectors(dut)

    b = []
    value = 1
    for i in range(LENGTH):
        b.append(value)
    await test_vectors(dut, 2, b)

    dut.in_valid.value = 0;
    for i in range(1000):
        await toggle_clk(dut);

@cocotb.test()
async def my_first_test(dut):
    global vec_sum
    await setup(dut)

    LENGTH = 80
    value = 1

    vec = []
    for i in range(LENGTH):
        vec.append(i)
    print(vec)
    print_vector_sum(vec)

    await load_vector(dut, LENGTH, 2, vec)

    await single_test(dut, LENGTH)

    await single_test(dut, LENGTH)

    await single_test(dut, LENGTH)

    if DEBUG==1: print_vector(dut.vector_a.value)

