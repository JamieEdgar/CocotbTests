import cocotb
from cocotb.triggers import Timer
import numpy as np

import sys
from pathlib import Path
proj_path = Path(__file__)
pkgs = proj_path.parent.parent.parent / 'NN_Packages/'
sys.path.append(str(pkgs))

from conversion_pkg import RealToHalf, DoubleFromHalf

DEBUG = 1
result_count = 0
calc_sum = 0
first_value = 1

async def toggle_clk(dut):
    global result_count
    global vec_sum
    global calc_sum
    global first_value
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if (dut.done.value == 1):
        result = VectorHalfToReal(dut.vector_c.value)
        print("result = ", result.index(max(result)))
        result_count += 1
        if result_count == 80:
            result_count = 0
    #print("sum", DoubleFromHalf(int(dut.sum.value)), calc_sum, first_value-1)

async def setup(dut):
    dut.start.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)
DoubleFromHalf
def VectorHalfToReal(vec):
    return [DoubleFromHalf(int(element)) for element in vec]

def VectorRealToHalf(vec):
    return [RealToHalf(element) for element in vec]


async def test_values(dut, vec):
    vec_half = VectorRealToHalf(vec)
    dut.vector_a.value = vec_half
    dut.start.value = 1
    await toggle_clk(dut)
    dut.start.value = 0

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))

vec_sum = 0

@cocotb.test()
async def my_first_test(dut):
    global vec_sum
    await setup(dut)

    LENGTH = 80

    vec = [1, 2, 3, 4, 5, 6, 7, 8]
    await test_values(dut, vec)
    vec = [1, 2, 30, 4, 5, 6, 7, 8]
    await test_values(dut, vec)
    vec = [1, 2, 3, 4, 5, 6, 7, 8]
    await test_values(dut, vec)
    for i in range(100):
        await toggle_clk(dut)
