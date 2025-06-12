import cocotb
from cocotb.triggers import Timer

async def toggle_clk(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")

async def test(dut, a, b):
    for i in range(10):
        dut.in_valid.value = 1
        dut.a.value = a
        dut.b.value = b
        await toggle_clk(dut)
        if (dut.out_valid == 1):
            print("result = ", dut.c.value.integer)

async def test2(dut, a):
    for i in range(10):
        dut.in_valid.value = 1
        dut.a.value = a
        dut.b.value = i+1
        await toggle_clk(dut)
        if (dut.out_valid == 1):
            print("result = ", dut.c.value.integer)


@cocotb.test()
async def my_first_test(dut):
    """Try accessing the design."""
    await test(dut, 3, 3)
    await test2(dut, 1)
    await test(dut, 4, 4)
    await test(dut, 5, 5)
    await test2(dut, 1)
    dut.in_valid.value = 0
    for i in range(10):
        await toggle_clk(dut)
        if (dut.out_valid == 1):
            print("result = ", dut.c.value.integer)
