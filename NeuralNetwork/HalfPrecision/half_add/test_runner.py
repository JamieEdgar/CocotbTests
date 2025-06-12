# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def half_add():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"
    faster_files_path = top_path / "NeuralNetwork/HalfPrecision/FasterFiles/"

    sources = [ files_path / "leading_zero_count.sv",
                files_path / "half_add.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_add"
    )

    runner.test(hdl_toplevel="half_add", test_module="half_add_test,")


if __name__ == "__main__":
    half_add()
