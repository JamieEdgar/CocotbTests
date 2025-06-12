# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def single_add_test():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"

    sources = [files_path / "leading_zero_count.sv",
               proj_path / "single_add_1clk.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="single_add_1clk"
    )

    runner.test(hdl_toplevel="single_add_1clk", test_module="single_add_test")


if __name__ == "__main__":
    single_add_test()
