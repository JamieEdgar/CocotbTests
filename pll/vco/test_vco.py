import cocotb
from cocotb.triggers import Timer
from matplotlib import pyplot as plt


@cocotb.test()
async def my_first_test(dut):
    """Try accessing the design."""
    print("Before cycle loop")
    previous = None
    count = 0
    dut.x.value = 0
    for cycle in range(5000):
        dut.clk.value = 0
        #dut.a.value = 5
        #dut.b.value = 5
        if (count % 500 == 0):
            if (dut.x.value + 50 < 255):
              dut.x.value = dut.x.value + 50
            else:
              dut.x.value = 50
        await Timer(1, units="ns")
        print("dut.x =", int(dut.x.value), "dut.y =", dut.y.value)
        dut.clk.value = 1
        count = count + 1
        if previous != None:
          plt.plot([previous[0], count], [previous[1],dut.y.value], '-')
          previous = count, dut.y.value
        else:
          plt.plot(count, dut.y.value, '-')
          previous = count, dut.y.value
        if (count % 50 == 0):
          plt.pause(0.001)
        #dut.a.value = 6
        #dut.b.value = 6
        await Timer(1, units="ns")
    print("After cycle loop")
    plt.show()
    #dut._log.info("my_signal_1 is %s a is %s b is %s c is %s", dut.my_signal_1.value , dut.a.value, dut.b.value, dut.c.value)
    #assert dut.my_signal_2.value[0] == 0, "my_signal_2[0] is not 0!"
