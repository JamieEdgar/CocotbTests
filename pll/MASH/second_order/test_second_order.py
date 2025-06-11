import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt

@cocotb.test()
async def my_first_test(dut):
    """Try accessing the design."""
    print("Before cycle loop")
    previous = None
    count = 0
    dut.f.value = 0
    for cycle in range(500):
        dut.clk.value = 0
        #dut.a.value = 5
        #dut.b.value = 5
        if (count % 200 == 0):
            if (dut.f.value + 50 < 255):
              dut.f.value = dut.f.value + 50
            else:
              dut.f.value = 50
        await Timer(1, units="ns")
        result = int(dut.dn.value)
        if result > 2:
          result = -1
        print("result =", result)
        dut.clk.value = 1
        count = count + 1
        if previous != None:
          plt.plot([previous[0], count], [previous[1],result], '-')
          previous = count, result
        else:
          plt.plot(count, result, '-')
          previous = count, result
        if (count % 50 == 0):
          plt.pause(0.001)
        #dut.a.value = 6
        #dut.b.value = 6
        await Timer(1, units="ns")
    print("After cycle loop")
    plt.show()
    #dut._log.info("my_signal_1 is %s a is %s b is %s c is %s", dut.my_signal_1.value , dut.a.value, dut.b.value, dut.c.value)
    #assert dut.my_signal_2.value[0] == 0, "my_signal_2[0] is not 0!"
