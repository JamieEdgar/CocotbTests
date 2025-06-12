import cocotb
from cocotb.triggers import Timer
import numpy as np
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
    if (dut.out_valid.value == 1):
        result = DoubleFromHalf(int(dut.c.value))
        print("result = ", result)
        result_count += 1
        if result_count == 80:
            result_count = 0
    if int(dut.sum.value) != 0:
        calc_sum += first_value
        first_value += 1
    #print("sum", DoubleFromHalf(int(dut.sum.value)), calc_sum, first_value-1)

async def setup(dut):
    dut.in_valid.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

async def test_values(dut, a, b):
    dut.a.value = RealToHalf(a)
    dut.b.value = RealToHalf(b)
    dut.in_valid.value = 1
    await toggle_clk(dut)
    dut.in_valid.value = 0
    #for i in range(100):
    #    await toggle_clk(dut)

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))

vec_sum = 0

@cocotb.test()
async def my_first_test(dut):
    global vec_sum
    await setup(dut)

    LENGTH = 80

    await test_values(dut, 1, 2)
    await test_values(dut, 2080, 65)        # This result is off by 1 due to the rounding error
