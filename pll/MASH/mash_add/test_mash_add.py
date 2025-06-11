import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt

async def toggle_clock(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")


async def test(dut, c, dn, dn_d):
    dut.c.value = c
    dut.dn.value = dn
    dut.dn_d.value = dn_d
    await toggle_clock(dut)
    result = int(dut.result.value)
    if result > 8:
        result = result - 16
    print(c, dn, dn_d, result)

@cocotb.test()
async def my_first_test(dut):
    """Try accessing the design."""
    print("Before cycle loop")
    previous = None
    count = 0

    for c in range(2):
        for dn in range(4):
            for dn_d in range(4):
                dn2 = dn
                dn_d2 = dn_d
                if dn_d2 == 3:
                    dn_d2 = 7
                if dn2 == 3:
                    dn2 = 7
                await test(dut, c, dn2, dn_d2)
