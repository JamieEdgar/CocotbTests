# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def test_second_order():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    #proj_path = "/home/jamie/git/j1s1e1/VerilogPolarCodes/test_bench/"

    sources = [proj_path / "stage.sv",
               proj_path / "second_order.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="second_order",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="second_order", test_module="test_second_order,")


if __name__ == "__main__":
    test_second_order()
