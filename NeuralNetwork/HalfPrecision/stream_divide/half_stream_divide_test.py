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
        print("c = ", DoubleFromHalf(int(dut.c.value)))

async def setup(dut):
    dut.in_valid.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

async def test_vectors(dut, a, b):
    c = int(len(a))
    for i in range(c):
        dut.a.value = RealToHalf(a[c-1-i])
        dut.b.value = RealToHalf(b[c-1-i])
        dut.in_valid.value = 1
        await toggle_clk(dut)
    dut.in_valid.value = 0

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))


@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    a = [1.33, 1.33, 1.33, 1.33, 1.33, 1.33, 1.33, 1.33, 1.33, 1.33]

    b = [1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45]

    await test_vectors(dut, a, b)

    await test_vectors(dut, a, b)

    dut.in_valid.value = 0
    for i in range(100):
        await toggle_clk(dut)

    for i in range(10):
        a[i] = a[i] * 2
    await test_vectors(dut, a, b)

    for i in range(10):
        a[i] = a[i] * 2
    await test_vectors(dut, a, b)

    a = [1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45]

    await test_vectors(dut, a, b)


    a = [-1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45]

    await test_vectors(dut, a, b)

    dut.in_valid.value = 0;
    for i in range(200):
        await toggle_clk(dut);

