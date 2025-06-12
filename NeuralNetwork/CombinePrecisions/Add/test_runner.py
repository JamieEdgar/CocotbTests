# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def combined_add_test_single():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"

    sources = [files_path / "leading_zero_count.sv",
               proj_path / "combined_add.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="combined_add"
    )

    runner.test(hdl_toplevel="combined_add", test_module="combined_add_test")

def combined_add_test_half():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"

    sources = [files_path / "leading_zero_count.sv",
               proj_path / "combined_add.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="combined_add",
        parameters={"WIDTH": 16, "EXP": 5}
    )

    runner.test(hdl_toplevel="combined_add", test_module="combined_add_test")

if __name__ == "__main__":
    combined_add_test_single()
    combined_add_test_half()
