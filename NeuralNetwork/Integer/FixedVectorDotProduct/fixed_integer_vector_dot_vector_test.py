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
    if (DEBUG == 4):
        print("dut.out_valid",  int(dut.out_valid.value))
        print("dut.c",  int(dut.c.value))
    if (DEBUG == 1):
        print("dut.in_valid",  int(dut.in_valid.value), end=" ")
        print("dut.count", int(dut.count.value), end=" ")
        print("dut.out_valid",  int(dut.out_valid.value))
    if (DEBUG == 6):
        a = []
        for i in range(10):
            a.append(int(dut.vector_a[i].value))
        print("dut.vector_a", a)


async def setup(dut):
    dut.in_valid.value = 0;
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

async def load_a(dut, mults, a):
    for i in range(int(len(a)/mults)):
        a_in = a[mults*i:mults*(i+1)]
        dut.vector_a_in.value = a_in
        dut.load_a.value = 1
        await toggle_clk(dut)
        dut.load_a.value = 0

async def test_vectors(dut, mults, b):
    for i in range(int(len(b)/mults)):
        b_in = b[mults*i:mults*(i+1)]
        dut.vector_b.value = b_in
        dut.in_valid.value = 1
        await toggle_clk(dut)

@cocotb.test()
async def my_first_test(dut):
    await setup(dut)

    a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    await load_a(dut, 2, a)

    b = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    await test_vectors(dut, 2, b)

    for i in range(10):
        b[i] = b[i] * 2
    await test_vectors(dut, 2, b)

    dut.in_valid.value = 0;
    for i in range(20):
        await toggle_clk(dut);

    for i in range(10):
        b[i] = b[i] * 2
    await test_vectors(dut, 2, b)

    b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print("b sum", sum(b))
    await test_vectors(dut, 2, b)

    dut.in_valid.value = 0;
    for i in range(20):
        await toggle_clk(dut);

