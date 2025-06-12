import cocotb
from cocotb.triggers import Timer

DEBUG=1

async def toggle_clk(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if (DEBUG == 1):
        print("count = ", int(dut.count.value), end=" ")
        print("sum = ", int(dut.sum.value))

async def test(dut, a):
    print("sum = ", a*10)
    for i in range(10):
        dut.in_valid.value = 1
        dut.a.value = a
        await toggle_clk(dut)
        if (dut.out_valid == 1):
            print("result = ", dut.c.value.integer)


@cocotb.test()
async def my_first_test(dut):
    """Try accessing the design."""
    await test(dut, 3)
    await test(dut, 4)
    await test(dut, 5)
    dut.in_valid.value = 0
    for i in range(10):
        await toggle_clk(dut)
        if (dut.out_valid == 1):
            print("result = ", dut.c.value.integer)
