import cocotb
from cocotb.triggers import Timer

DEBUG = 1

async def toggle_clk(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if (dut.out_valid.value == 1):
        print("result = ", int(dut.c.value))
    if (DEBUG == 2):
        print("dut.c_mult[0]",  int(dut.c_mult[0].value))
        print("dut.c_mult[1]",  int(dut.c_mult[1].value))
    if (DEBUG == 3):
        print("dut.sum_in",  int(dut.sum_in.value))
        print("dut.in_valid_add",  int(dut.in_valid_add.value))
    if (DEBUG == 3):
        print("dut.out_valid",  int(dut.out_valid.value))
        print("dut.sum",  int(dut.sum.value))


async def setup(dut):
    dut.in_valid.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

async def test_vectors(dut, mults, a, b):
    for i in range(int(len(a)/mults)):
        a_in = a[mults*i:mults*(i+1)]
        dut.vector_a.value = a_in
        b_in = b[mults*i:mults*(i+1)]
        dut.vector_b.value = b_in
        dut.in_valid.value = 1
        await toggle_clk(dut)



@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    b = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    a = a + a + a;
    b = b + b + b
    await test_vectors(dut, 3, a, b)

    for i in range(10):
        a[i] = a[i] * 2
    await test_vectors(dut, 3, a, b)

    for i in range(10):
        a[i] = a[i] * 2
    await test_vectors(dut, 3, a, b)

    dut.in_valid.value = 0;
    for i in range(10):
        await toggle_clk(dut);

