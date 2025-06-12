import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt
import numpy as np
import Precision as Prec

Prec.debug = False
debug = False

displayed = False

async def reset(dut):
    dut.rstn.value = 1
    await clock_cycle(dut)
    dut.rstn.value = 0
    await clock_cycle(dut)
    dut.rstn.value = 1
    await clock_cycle(dut)


async def clock_cycle(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")

async def add_test(dut, a, b):
    dut.in_valid.value = 1;
    dut.a.value = Prec.BinToInt(Prec.HalfToBinary(a))
    dut.b.value = Prec.BinToInt(Prec.HalfToBinary(b))
    await clock_cycle(dut)
    if dut.out_valid.value == 1:
        print("out valid = 1")
        if (debug): print("agtb", dut.a_gt_b.value)
        if (debug): print("shifts", int(dut.ashift.value), int(dut.bshift.value))
        if (debug): print("leading zeros", int(dut.leading_zeros.value))
        if (debug): print(dut.a.value, dut.b.value, dut.c.value)
        print(Prec.BinaryToHalf(str(dut.a.value)),
              Prec.BinaryToHalf(str(dut.b.value)),
              Prec.BinaryToHalf(str(dut.c.value)))
        print(dut.sum.value)
    dut.in_valid.value = 0;
    await clock_cycle(dut)

@cocotb.test()
async def my_first_test(dut):
    global displayed
    """Try accessing the design."""

    dut.in_valid.value = 0
    await clock_cycle(dut)

    await reset(dut)

    await add_test(dut, 0.1, 0.1)
    await add_test(dut, 0.1, -0.1)
    await add_test(dut, 127, 0.1)
    await add_test(dut, 127, 0)
    await add_test(dut, 0.1, 3e4)
    await add_test(dut, 4e-4, 3e4)
    await add_test(dut, 4e-3, 3e4)
    await add_test(dut, 4e-2, 3e4)
    await add_test(dut, 4e-1, 3e4)
    await add_test(dut, 16, 3e4)



    #dut._log.info("my_signal_1 is %s a is %s b is %s c is %s", dut.my_signal_1.value , dut.a.value, dut.b.value, dut.c.value)
    #assert dut.my_signal_2.value[0] == 0, "my_signal_2[0] is not 0!"
