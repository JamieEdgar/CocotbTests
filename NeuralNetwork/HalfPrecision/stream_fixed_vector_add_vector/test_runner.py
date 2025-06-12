# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def half_fixed_vector_add_vector():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"
    faster_files_path = top_path / "NeuralNetwork/HalfPrecision/FasterFiles/"

    sources = [ files_path / "leading_zero_count.sv",
                files_path / "half_add.sv",
                faster_files_path / "half_fixed_vector_add_vector.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_fixed_vector_add_vector",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="half_fixed_vector_add_vector", test_module="half_fixed_vector_add_vector_test,")


if __name__ == "__main__":
    half_fixed_vector_add_vector()
