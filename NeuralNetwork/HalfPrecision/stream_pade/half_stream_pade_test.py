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
    if (DEBUG == 2):
        print("c = ", DoubleFromHalf(int(dut.c.value)))
    if (DEBUG == 3):
        print("half_pade_1.px2 = ", DoubleFromHalf(int(dut.half_pade_1.px2.value)), end=" ")
        print("half_pade_1.fpart_sqr_d3 = ", DoubleFromHalf(int(dut.half_pade_1.fpart_sqr_d3.value)))
    if (DEBUG == 4):
        print("half_pade_1.px3 = ", DoubleFromHalf(int(dut.half_pade_1.px3.value)), end=" ")
        print("half_pade_1.fm_exp2_p[0] = ", DoubleFromHalf(int(dut.half_pade_1.fm_exp2_p[0].value)))
    if (DEBUG == 3):
        print("half_pade_1.qx = ", DoubleFromHalf(int(dut.half_pade_1.qx.value)), end=" ")
        print("half_pade_1.fpart_sqr_d1 = ", DoubleFromHalf(int(dut.half_pade_1.fpart_sqr_d1.value)))
    if (DEBUG == 4):
        print("half_pade_1.qx2 = ", DoubleFromHalf(int(dut.half_pade_1.qx2.value)), end=" ")
        print("half_pade_1.fm_exp2_q[1] = ", DoubleFromHalf(int(dut.half_pade_1.fm_exp2_q[1].value)))
    if (DEBUG == 2):
        print("half_pade_1.px4 = ", DoubleFromHalf(int(dut.half_pade_1.px4.value)), end=" ")
        print("half_pade_1.fpart_d8 = ", DoubleFromHalf(int(dut.half_pade_1.fpart_d8.value)))
    if (DEBUG == 2):
        print("half_pade_1.qx3_d4 = ", DoubleFromHalf(int(dut.half_pade_1.qx3_d4.value)), end=" ")
        print("half_pade_1.px5 = ", DoubleFromHalf(int(dut.half_pade_1.px5.value)))
    if (DEBUG == 1):
        print("half_pade_1.px5_d1 = ", DoubleFromHalf(int(dut.half_pade_1.px5_d1.value)), end=" ")
        print("half_pade_1.qx3_m_px5 = ", DoubleFromHalf(int(dut.half_pade_1.qx3_m_px5.value)), end=" ")
        print("half_pade_1.px5_d_qx3_m_px5 = ", DoubleFromHalf(int(dut.half_pade_1.px5_d_qx3_m_px5.value)))
    if (DEBUG == 2):
        print("half_pade_1.px5_d_qx3_m_px5 = ", DoubleFromHalf(int(dut.half_pade_1.px5_d_qx3_m_px5.value)), end=" ")
        print("half_pade_1.px5_d_qx3_m_px5_m_2 = ", DoubleFromHalf(int(dut.half_pade_1.px5_d_qx3_m_px5_m_2.value)))


async def setup(dut):
    dut.in_valid.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

async def test_vectors(dut, a):
    c = int(len(a))
    for i in range(c):
        dut.a.value = RealToHalf(a[c-1-i])
        dut.in_valid.value = 1
        await toggle_clk(dut)
    dut.in_valid.value = 0

async def check_vectors(dut):
    await toggle_clk(dut)
    #print("v0", int(dut.vector_dps[0].vector_a.value))


@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    a = [1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45]

    await test_vectors(dut, a)

    await test_vectors(dut, a)

    dut.in_valid.value = 0
    for i in range(100):
        await toggle_clk(dut)

    for i in range(10):
        a[i] = a[i] * 2
    await test_vectors(dut, a)

    for i in range(10):
        a[i] = a[i] * 2
    await test_vectors(dut, a)

    a = [1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45, 1.45]

    await test_vectors(dut, a)


    a = [-1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45, -1.45]

    await test_vectors(dut, a)

    dut.in_valid.value = 0;
    for i in range(100):
        await toggle_clk(dut);

